================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### Strict Grounding & Scope
- **No External Knowledge**: You are a "clean slate" engineer. Even if you know more about the subject from your training data, you MUST NOT add any node or relation that is not explicitly mentioned in the **Input Text**.
- **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
- **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target is a critical failure that invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly (in your thought process) perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it. Source is always to the left of a relation.
* **The Target**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon. Target is always to the right of a relation.

#### 3. Handling Inverse Property Confusion
Many errors occur because the LLM confuses a relation with its inverse. You must be hyper-vigilant:
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**


### Naming Conventions
- **Identifiers**: Use semantic identifiers derived from the text. 
- **Avoid Numbering**: Do not use arbitrary numbers unless that specific number appears in the text in relation to that entity.
- **Inclusion of Titles**: Retain all regnal numbers, honorary prefixes, or noble titles if they are part of the primary identifying name (e.g., "Crown Prince [Name]" or "[Name] II").
- **Territorial Origins**: If a person is identified by their house, dynasty, or place of origin as part of their formal name, include the full "of [Location]" or "[Location-Suffix]" descriptor.
- **Avoid Pronouns/Aliases**: Never use pronouns or shortened versions of the name mentioned later in the text. Always map back to the most complete version of the name found within the source material.

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **Finish**: Once you are finished, use this tool.
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
Prince Christoph of Hesse (Christoph Ernst August; 14
May 1901 – 7 October 1943) was a nephew of Kaiser Wilhelm II.
His brother-in-law Prince Philip of Greece and Denmark fought on the British side and married the future Queen Elizabeth II after the war.
Birth

Prince Christoph of Hesse was born in Frankfurt, the fifth son of Prince Frederick Charles of Hesse and Princess Margaret of Prussia.
He was a twin, with Prince Richard of Hesse.
His father, Frederick Charles, a scion of the House of Hesse, was elected King of Finland in 1918, when Finland declared its independence after the collapse of the Russian Empire.
Christoph's mother was the daughter of Emperor Frederick III and of Victoria, Princess Royal.
Prince Christoph was thus a great-grandson of Queen Victoria and Prince Albert of Saxe-Coburg and Gotha.
Christoph had several brothers, including Prince Philipp and Prince Wolfgang.
His two eldest brothers, Friedrich Wilhelm and Maximilian, both died in World War I.


Career and death

Prince Christoph was a director in the Third Reich's Ministry of Air Forces, Commander of the Air Reserves, and held the rank of Oberführer in the SS.
His brother Prince Philipp joined Hitler's SA.
They were not the only family members to embrace Nazism; their mother "Mossy" (a sister of Kaiser Wilhelm II) invited Adolf Hitler to tea and flew the swastika from her home at Schloss Kronberg.
According to the historian Hugo Vickers, Prince Christoph became "disenchanted" with the Nazi Party by the time of the assassination of Reinhard Heydrich in 1942.
"


Prince Christoph served in the Luftwaffe Research Office and, in 1942, he joined the staff of a fighter unit, Jagdgeschwader 53.
After the Allied Invasion of Italy, Christoph was recalled to Germany, but was killed during his return.
His body and the body of his copilot Wilhelm Gsteu were found two days later and were buried in a German military cemetery near Forlì.
Family

Christoph married his second cousin, once removed, Princess Sophie of Greece and Denmark on 15 December 1930 in Kronberg im Taunus, Germany.
Princess Sophie was the youngest daughter of Prince Andrew of Greece and Denmark and Princess Alice of Battenberg, and the sister of the future Prince Philip, Duke of Edinburgh.
The couple had five children:


Some years after Christoph's death, his widow married Prince George William of Hanover, a brother of Queen Fredrica of Greece and a grandson of Kaiser Wilhelm II.
Four years after Christoph's death, his widow's brother, Philip, married the future Queen Elizabeth II.
Christoph's surviving children are first cousins of King Charles III.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

: a owl:Ontology ;
    dcterms:source <http://www.co-ode.org/roberts/family-tree.owl> .

:alsoKnownAs a owl:AnnotationProperty .

:formerlyKnownAs a owl:AnnotationProperty .

:hasBirthYear a rdfs:Datatype,
        owl:AnnotationProperty .

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

:isAuntOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isSisterOf :isParentOf ) .

:isUncleOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isBrotherOf :isParentOf ) .

:knownAs a owl:AnnotationProperty .

dcterms:source a owl:AnnotationProperty .

ns2:isRuleEnabled a owl:AnnotationProperty .

:hasBrother a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isBrotherOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasDaughter a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isDaughterOf .

:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Man ;
    rdfs:subPropertyOf :hasParent ;
    owl:inverseOf :isFatherOf .

:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Woman ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf ;
    owl:inverseOf :isMotherOf .

:hasSister a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isSisterOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasSon a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isSonOf .

:isBloodrelationOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty .

:isDaughterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:isFatherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isMotherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isSonOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:DomainEntity a owl:Class .

:Female a owl:Class ;
    rdfs:subClassOf :Sex ;
    owl:disjointWith :Male .

:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf :isAncestorOf .

:isBrotherOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:Male a owl:Class ;
    rdfs:subClassOf :Sex .

:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person .

:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Sex .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns1:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns1:Variable .

:Ancestor a owl:Class ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :isAncestorOf ;
                        owl:someValuesFrom :Person ] ) ] .

:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty :hasFather ;
            owl:someValuesFrom :Man ],
        [ a owl:Restriction ;
            owl:onProperty :hasMother ;
            owl:someValuesFrom :Woman ],
        [ a owl:Restriction ;
            owl:onProperty :hasSex ;
            owl:someValuesFrom :Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass :Person ;
            owl:onProperty :hasParent ],
        :DomainEntity ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Man :Woman ) ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (e6a051c7-ffeb-4c68-95eb-742808070958)
 Call ID: e6a051c7-ffeb-4c68-95eb-742808070958
  Args:
    source: Prince_Christoph_of_Hesse
    type: :Man
  AssignClass (1af9a19b-1ec6-4286-aba9-1cb8438287a3)
 Call ID: 1af9a19b-1ec6-4286-aba9-1cb8438287a3
  Args:
    type: :Person
    source: Prince_Christoph_of_Hesse
  AddLiteral (ac636dfc-822d-4d97-bf23-ec565cdb0469)
 Call ID: ac636dfc-822d-4d97-bf23-ec565cdb0469
  Args:
    relation: :hasBirthYear
    literal_value: 1901
    source: Prince_Christoph_of_Hesse
    literal_type: xsd:integer
  AddLiteral (52830f5e-2a0b-4213-b337-1d4ebb4cb71e)
 Call ID: 52830f5e-2a0b-4213-b337-1d4ebb4cb71e
  Args:
    literal_value: 1943
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Prince_Christoph_of_Hesse
  AssignClass (5af67548-14c3-4f43-921d-ce324284dcff)
 Call ID: 5af67548-14c3-4f43-921d-ce324284dcff
  Args:
    source: Prince_Frederick_Charles_of_Hesse
    type: :Man
  AssignClass (906b1b76-df50-46f4-ad2a-d9b3a63f6899)
 Call ID: 906b1b76-df50-46f4-ad2a-d9b3a63f6899
  Args:
    type: :Person
    source: Prince_Frederick_Charles_of_Hesse
  AssignClass (0e810aeb-83d7-4fa7-90fb-b88e719dac13)
 Call ID: 0e810aeb-83d7-4fa7-90fb-b88e719dac13
  Args:
    source: Princess_Margaret_of_Prussia
    type: :Woman
  AssignClass (9339972a-3a30-4719-b57d-e80cf778368e)
 Call ID: 9339972a-3a30-4719-b57d-e80cf778368e
  Args:
    source: Princess_Margaret_of_Prussia
    type: :Person
  AddTriple (9a411c73-22a7-43e9-819d-619e5008cc78)
 Call ID: 9a411c73-22a7-43e9-819d-619e5008cc78
  Args:
    source: Prince_Christoph_of_Hesse
    target: Prince_Frederick_Charles_of_Hesse
    relation: :hasFather
  AddTriple (2b3a0a96-a708-4de0-9490-2a41512ba4a1)
 Call ID: 2b3a0a96-a708-4de0-9490-2a41512ba4a1
  Args:
    source: Prince_Christoph_of_Hesse
    relation: :hasMother
    target: Princess_Margaret_of_Prussia
  AssignClass (932b805e-46c2-4ba8-a399-ed7f1d634287)
 Call ID: 932b805e-46c2-4ba8-a399-ed7f1d634287
  Args:
    source: Prince_Richard_of_Hesse
    type: :Man
  AssignClass (9ab3e90a-f29f-42a5-b656-a2b50ee1b898)
 Call ID: 9ab3e90a-f29f-42a5-b656-a2b50ee1b898
  Args:
    type: :Person
    source: Prince_Richard_of_Hesse
  AddTriple (dc584c2e-ed75-45a4-bc3b-ef54ecf101ce)
 Call ID: dc584c2e-ed75-45a4-bc3b-ef54ecf101ce
  Args:
    source: Prince_Christoph_of_Hesse
    relation: :isSiblingOf
    target: Prince_Richard_of_Hesse
  AssignClass (8ce8e51c-c2f9-48d8-ac18-f66a1cc30b45)
 Call ID: 8ce8e51c-c2f9-48d8-ac18-f66a1cc30b45
  Args:
    type: :Man
    source: Emperor_Frederick_III
  AssignClass (9bc645e1-0206-4020-b584-9ae00d1cb814)
 Call ID: 9bc645e1-0206-4020-b584-9ae00d1cb814
  Args:
    source: Emperor_Frederick_III
    type: :Person
  AssignClass (66ad0f75-2f52-439f-87b5-fa11968b1080)
 Call ID: 66ad0f75-2f52-439f-87b5-fa11968b1080
  Args:
    source: Victoria_Princess_Royal
    type: :Woman
  AssignClass (3140f292-c2bc-4983-9e4d-121b1b9b346d)
 Call ID: 3140f292-c2bc-4983-9e4d-121b1b9b346d
  Args:
    source: Victoria_Princess_Royal
    type: :Person
  AddTriple (6be9612d-29f6-4581-bd6a-48df18257b75)
 Call ID: 6be9612d-29f6-4581-bd6a-48df18257b75
  Args:
    target: Emperor_Frederick_III
    relation: :hasFather
    source: Princess_Margaret_of_Prussia
  AddTriple (a20225f7-f7ec-4c08-8cbf-7cdf4de84eb5)
 Call ID: a20225f7-f7ec-4c08-8cbf-7cdf4de84eb5
  Args:
    relation: :hasMother
    target: Victoria_Princess_Royal
    source: Princess_Margaret_of_Prussia
  AssignClass (38f24001-9907-49fd-917f-bc6242bc586c)
 Call ID: 38f24001-9907-49fd-917f-bc6242bc586c
  Args:
    source: Prince_Philipp_of_Hesse
    type: :Man
  AssignClass (14e97d34-dbd2-4cf8-bdea-aeecd47837b0)
 Call ID: 14e97d34-dbd2-4cf8-bdea-aeecd47837b0
  Args:
    type: :Person
    source: Prince_Philipp_of_Hesse
  AssignClass (b27ae382-8d9d-462a-8291-a82de6ef2f5b)
 Call ID: b27ae382-8d9d-462a-8291-a82de6ef2f5b
  Args:
    source: Prince_Wolfgang_of_Hesse
    type: :Man
  AssignClass (7f78ae2c-0f71-4b08-9a4b-b9db1f20d55e)
 Call ID: 7f78ae2c-0f71-4b08-9a4b-b9db1f20d55e
  Args:
    source: Prince_Wolfgang_of_Hesse
    type: :Person
  AssignClass (d9b855d7-2d4f-47b6-b6ef-d1ba32dd2504)
 Call ID: d9b855d7-2d4f-47b6-b6ef-d1ba32dd2504
  Args:
    source: Friedrich_Wilhelm_of_Hesse
    type: :Man
  AssignClass (42e96feb-5845-4be2-9fe4-bea485483a70)
 Call ID: 42e96feb-5845-4be2-9fe4-bea485483a70
  Args:
    source: Friedrich_Wilhelm_of_Hesse
    type: :Person
  AssignClass (46ba9cd4-d989-4075-9f72-625bf1c4f6be)
 Call ID: 46ba9cd4-d989-4075-9f72-625bf1c4f6be
  Args:
    source: Maximilian_of_Hesse
    type: :Man
  AssignClass (21251ebc-7c16-44f7-a1b9-db5e8f33da63)
 Call ID: 21251ebc-7c16-44f7-a1b9-db5e8f33da63
  Args:
    source: Maximilian_of_Hesse
    type: :Person
  AddTriple (2991df7d-df4b-4f01-a607-0fa8ca66b962)
 Call ID: 2991df7d-df4b-4f01-a607-0fa8ca66b962
  Args:
    relation: :isSiblingOf
    target: Prince_Philipp_of_Hesse
    source: Prince_Christoph_of_Hesse
  AddTriple (570adaa6-85cb-4677-a682-b8fe6282d5be)
 Call ID: 570adaa6-85cb-4677-a682-b8fe6282d5be
  Args:
    source: Prince_Christoph_of_Hesse
    relation: :isSiblingOf
    target: Prince_Wolfgang_of_Hesse
  AddTriple (9a5e2a7f-0287-4e90-b8b7-c0a0182eff23)
 Call ID: 9a5e2a7f-0287-4e90-b8b7-c0a0182eff23
  Args:
    source: Prince_Christoph_of_Hesse
    target: Friedrich_Wilhelm_of_Hesse
    relation: :isSiblingOf
  AddTriple (fb3f44f6-2a6a-491f-87d4-5c6c264c2969)
 Call ID: fb3f44f6-2a6a-491f-87d4-5c6c264c2969
  Args:
    target: Maximilian_of_Hesse
    relation: :isSiblingOf
    source: Prince_Christoph_of_Hesse
  AssignClass (bb7eecf8-4ff6-4f95-bda8-b670f3b7a1b4)
 Call ID: bb7eecf8-4ff6-4f95-bda8-b670f3b7a1b4
  Args:
    type: :Woman
    source: Princess_Sophie_of_Greece_and_Denmark
  AssignClass (cf870183-2cd7-44eb-be44-63e1949c8f70)
 Call ID: cf870183-2cd7-44eb-be44-63e1949c8f70
  Args:
    source: Princess_Sophie_of_Greece_and_Denmark
    type: :Person
  AddLiteral (bf9796ad-15e7-4be4-980d-5ae2ed4d46e5)
 Call ID: bf9796ad-15e7-4be4-980d-5ae2ed4d46e5
  Args:
    relation: :hasMarriageYear
    literal_value: 1930
    literal_type: xsd:integer
    source: Prince_Christoph_of_Hesse
  AddTriple (d94c8981-f820-403a-bc11-170c100db785)
 Call ID: d94c8981-f820-403a-bc11-170c100db785
  Args:
    source: Prince_Christoph_of_Hesse
    target: Princess_Sophie_of_Greece_and_Denmark
    relation: :hasRelation
  AssignClass (72d997eb-84f2-454a-9510-2cec00824690)
 Call ID: 72d997eb-84f2-454a-9510-2cec00824690
  Args:
    type: :Man
    source: Prince_Andrew_of_Greece_and_Denmark
  AssignClass (63b610f6-8cc3-4de2-82d8-96ecfa7a2167)
 Call ID: 63b610f6-8cc3-4de2-82d8-96ecfa7a2167
  Args:
    source: Prince_Andrew_of_Greece_and_Denmark
    type: :Person
  AssignClass (87cb63fe-67d2-4942-9dc4-3ff061895655)
 Call ID: 87cb63fe-67d2-4942-9dc4-3ff061895655
  Args:
    type: :Woman
    source: Princess_Alice_of_Battenberg
  AssignClass (73117173-84b1-4cac-97dc-01ee5b785f94)
 Call ID: 73117173-84b1-4cac-97dc-01ee5b785f94
  Args:
    source: Princess_Alice_of_Battenberg
    type: :Person
  AddTriple (5854359e-3b1d-4fc4-b18d-0f807a02171b)
 Call ID: 5854359e-3b1d-4fc4-b18d-0f807a02171b
  Args:
    target: Prince_Andrew_of_Greece_and_Denmark
    relation: :hasFather
    source: Princess_Sophie_of_Greece_and_Denmark
  AddTriple (ed0bfed4-3cbc-4528-bc39-dd99dd7dd90a)
 Call ID: ed0bfed4-3cbc-4528-bc39-dd99dd7dd90a
  Args:
    target: Princess_Alice_of_Battenberg
    relation: :hasMother
    source: Princess_Sophie_of_Greece_and_Denmark
  AssignClass (ac983213-7a48-4aeb-8551-b164711b3d37)
 Call ID: ac983213-7a48-4aeb-8551-b164711b3d37
  Args:
    source: Prince_Philip_Duke_of_Edinburgh
    type: :Man
  AssignClass (ae4a84ba-1463-41f3-833d-5813ef1affaa)
 Call ID: ae4a84ba-1463-41f3-833d-5813ef1affaa
  Args:
    type: :Person
    source: Prince_Philip_Duke_of_Edinburgh
  AddTriple (0353737f-4fd8-4adc-a267-c5854ca95a41)
 Call ID: 0353737f-4fd8-4adc-a267-c5854ca95a41
  Args:
    target: Prince_Philip_Duke_of_Edinburgh
    relation: :isSiblingOf
    source: Princess_Sophie_of_Greece_and_Denmark
  AssignClass (7b4c1a6a-1ba0-456e-b4db-8b99c2d61c49)
 Call ID: 7b4c1a6a-1ba0-456e-b4db-8b99c2d61c49
  Args:
    type: :Man
    source: Prince_George_William_of_Hanover
  AssignClass (8413a2e1-681a-40d8-929f-ad91ccacb922)
 Call ID: 8413a2e1-681a-40d8-929f-ad91ccacb922
  Args:
    source: Prince_George_William_of_Hanover
    type: :Person
  AddTriple (b2187ac5-9a70-43a7-9755-59356f644b74)
 Call ID: b2187ac5-9a70-43a7-9755-59356f644b74
  Args:
    target: Prince_George_William_of_Hanover
    relation: :hasRelation
    source: Princess_Sophie_of_Greece_and_Denmark
  Finish (57444fdc-cb1b-45c1-baf5-8d0e3413689f)
 Call ID: 57444fdc-cb1b-45c1-baf5-8d0e3413689f
  Args: