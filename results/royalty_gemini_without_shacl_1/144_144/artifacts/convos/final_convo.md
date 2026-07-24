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
  AssignClass (4b8b0cbc-598e-4d34-a996-a106ea802629)
 Call ID: 4b8b0cbc-598e-4d34-a996-a106ea802629
  Args:
    source: Prince Christoph of Hesse
    type: :Man
  AddLiteral (580b0ba9-3972-4a10-8f4d-66ff3eb01772)
 Call ID: 580b0ba9-3972-4a10-8f4d-66ff3eb01772
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1901
    source: Prince Christoph of Hesse
  AddLiteral (0ce62146-1b69-4ddd-a50a-43fd230f0595)
 Call ID: 0ce62146-1b69-4ddd-a50a-43fd230f0595
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1943
    source: Prince Christoph of Hesse
  AssignClass (6de8c0b7-68e0-43f5-847c-db6ae85f5c96)
 Call ID: 6de8c0b7-68e0-43f5-847c-db6ae85f5c96
  Args:
    type: :Man
    source: Kaiser Wilhelm II
  AssignClass (ff6ea9da-4126-4902-9016-16da829c136b)
 Call ID: ff6ea9da-4126-4902-9016-16da829c136b
  Args:
    source: Prince Philip of Greece and Denmark
    type: :Man
  AssignClass (22f744bc-e99d-47d2-9d03-95824ef62096)
 Call ID: 22f744bc-e99d-47d2-9d03-95824ef62096
  Args:
    source: Queen Elizabeth II
    type: :Woman
  AssignClass (6ed20563-debd-4358-8d55-0a37c0352b10)
 Call ID: 6ed20563-debd-4358-8d55-0a37c0352b10
  Args:
    source: Prince Frederick Charles of Hesse
    type: :Man
  AssignClass (3490f9b3-4231-4e42-823e-6e667c691428)
 Call ID: 3490f9b3-4231-4e42-823e-6e667c691428
  Args:
    source: Princess Margaret of Prussia
    type: :Woman
  AddTriple (c39361fb-0e4b-41c7-a496-e66cd8daef2e)
 Call ID: c39361fb-0e4b-41c7-a496-e66cd8daef2e
  Args:
    relation: :hasFather
    target: Prince Frederick Charles of Hesse
    source: Prince Christoph of Hesse
  AddTriple (277fbe67-bf02-4052-bf58-f0a1489991cf)
 Call ID: 277fbe67-bf02-4052-bf58-f0a1489991cf
  Args:
    relation: :hasMother
    source: Prince Christoph of Hesse
    target: Princess Margaret of Prussia
  AssignClass (470abdd6-ba8f-4f54-8022-abd8e5bdff83)
 Call ID: 470abdd6-ba8f-4f54-8022-abd8e5bdff83
  Args:
    source: Prince Richard of Hesse
    type: :Man
  AddTriple (61439628-91a9-4873-8b8f-7d015db46ccc)
 Call ID: 61439628-91a9-4873-8b8f-7d015db46ccc
  Args:
    relation: :isSiblingOf
    source: Prince Christoph of Hesse
    target: Prince Richard of Hesse
  AssignClass (19c38b85-8e11-4074-b2f4-07e8deb09860)
 Call ID: 19c38b85-8e11-4074-b2f4-07e8deb09860
  Args:
    type: :Man
    source: Emperor Frederick III
  AssignClass (fd8d6b6e-2eee-47bd-991f-dd9560823b7b)
 Call ID: fd8d6b6e-2eee-47bd-991f-dd9560823b7b
  Args:
    type: :Woman
    source: Victoria, Princess Royal
  AddTriple (c37f179c-e8ff-4dae-8c96-6eb2ef3296d4)
 Call ID: c37f179c-e8ff-4dae-8c96-6eb2ef3296d4
  Args:
    source: Princess Margaret of Prussia
    target: Emperor Frederick III
    relation: :hasFather
  AddTriple (93c1b4dd-6632-4e67-bc7a-858921d53bbb)
 Call ID: 93c1b4dd-6632-4e67-bc7a-858921d53bbb
  Args:
    relation: :hasMother
    source: Princess Margaret of Prussia
    target: Victoria, Princess Royal
  AssignClass (aa7df831-cd25-4117-b4c0-e0c1058748c8)
 Call ID: aa7df831-cd25-4117-b4c0-e0c1058748c8
  Args:
    type: :Woman
    source: Queen Victoria
  AssignClass (352b4a10-35f8-4413-b132-1f4cfdfc6f2e)
 Call ID: 352b4a10-35f8-4413-b132-1f4cfdfc6f2e
  Args:
    type: :Man
    source: Prince Albert of Saxe-Coburg and Gotha
  AssignClass (760a450f-25d6-4b3e-806a-b06ac1428500)
 Call ID: 760a450f-25d6-4b3e-806a-b06ac1428500
  Args:
    source: Prince Philipp of Hesse
    type: :Man
  AssignClass (588ddcba-1b4c-4f4c-a5e1-8dfaeca13a05)
 Call ID: 588ddcba-1b4c-4f4c-a5e1-8dfaeca13a05
  Args:
    source: Prince Wolfgang of Hesse
    type: :Man
  AssignClass (4256031e-1838-4e9a-8da1-9ab7402bf55d)
 Call ID: 4256031e-1838-4e9a-8da1-9ab7402bf55d
  Args:
    source: Friedrich Wilhelm of Hesse
    type: :Man
  AssignClass (d06df96d-cf2c-439f-a0f4-ee5b7775eb39)
 Call ID: d06df96d-cf2c-439f-a0f4-ee5b7775eb39
  Args:
    source: Maximilian of Hesse
    type: :Man
  AddTriple (db4f93ae-b26c-4868-9126-d624c73662d4)
 Call ID: db4f93ae-b26c-4868-9126-d624c73662d4
  Args:
    relation: :isSiblingOf
    target: Prince Philipp of Hesse
    source: Prince Christoph of Hesse
  AddTriple (8c640f91-7b05-4561-bfba-616609bccd75)
 Call ID: 8c640f91-7b05-4561-bfba-616609bccd75
  Args:
    target: Prince Wolfgang of Hesse
    source: Prince Christoph of Hesse
    relation: :isSiblingOf
  AddTriple (93743d9e-3082-4836-9a23-bee1221d573f)
 Call ID: 93743d9e-3082-4836-9a23-bee1221d573f
  Args:
    source: Prince Christoph of Hesse
    target: Friedrich Wilhelm of Hesse
    relation: :isSiblingOf
  AddTriple (7561a272-c046-4db4-ac1b-c387ef01a4db)
 Call ID: 7561a272-c046-4db4-ac1b-c387ef01a4db
  Args:
    target: Maximilian of Hesse
    source: Prince Christoph of Hesse
    relation: :isSiblingOf
  AssignClass (cb025dcc-758f-44b2-83ad-949ee2e38fef)
 Call ID: cb025dcc-758f-44b2-83ad-949ee2e38fef
  Args:
    source: Princess Sophie of Greece and Denmark
    type: :Woman
  AddTriple (7efcbfb9-65ef-4985-b4ac-591fb355d7e2)
 Call ID: 7efcbfb9-65ef-4985-b4ac-591fb355d7e2
  Args:
    source: Prince Christoph of Hesse
    target: Princess Sophie of Greece and Denmark
    relation: :hasRelation
  AddLiteral (aaed1ed6-2d27-4355-8c5d-cb9b1423c146)
 Call ID: aaed1ed6-2d27-4355-8c5d-cb9b1423c146
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1930
    source: Prince Christoph of Hesse
  AssignClass (0c8a2217-c0a2-45dc-ac59-b9a29c1e51b7)
 Call ID: 0c8a2217-c0a2-45dc-ac59-b9a29c1e51b7
  Args:
    type: :Man
    source: Prince Andrew of Greece and Denmark
  AssignClass (b2d96baf-8fe4-4f45-9388-5937078d43d6)
 Call ID: b2d96baf-8fe4-4f45-9388-5937078d43d6
  Args:
    type: :Woman
    source: Princess Alice of Battenberg
  AddTriple (d7086c30-d0ab-4c79-b4a4-e52b2ae8346c)
 Call ID: d7086c30-d0ab-4c79-b4a4-e52b2ae8346c
  Args:
    relation: :hasFather
    source: Princess Sophie of Greece and Denmark
    target: Prince Andrew of Greece and Denmark
  AddTriple (3e91ca09-4d69-45d0-b4bc-db2d8e1dd6a8)
 Call ID: 3e91ca09-4d69-45d0-b4bc-db2d8e1dd6a8
  Args:
    source: Princess Sophie of Greece and Denmark
    target: Princess Alice of Battenberg
    relation: :hasMother
  AddTriple (d8db7804-f270-49cf-99b9-a3f0985e9002)
 Call ID: d8db7804-f270-49cf-99b9-a3f0985e9002
  Args:
    source: Princess Sophie of Greece and Denmark
    target: Prince Philip of Greece and Denmark
    relation: :isSisterOf
  AssignClass (c44b90e8-7f70-4e6a-8955-bb0b31e48e45)
 Call ID: c44b90e8-7f70-4e6a-8955-bb0b31e48e45
  Args:
    source: Prince George William of Hanover
    type: :Man
  AssignClass (f756c9c0-1abf-4a90-8d76-4cac9488a63b)
 Call ID: f756c9c0-1abf-4a90-8d76-4cac9488a63b
  Args:
    type: :Woman
    source: Queen Fredrica of Greece
  AddTriple (4a48f284-8ee7-4a81-9f66-733ec1bd4935)
 Call ID: 4a48f284-8ee7-4a81-9f66-733ec1bd4935
  Args:
    target: Queen Fredrica of Greece
    source: Prince George William of Hanover
    relation: :isBrotherOf
  AssignClass (e028b76e-f46f-42ed-bbae-8bdb2f345b81)
 Call ID: e028b76e-f46f-42ed-bbae-8bdb2f345b81
  Args:
    source: King Charles III
    type: :Man
  Finish (35ccbf64-288f-4ec2-96f7-242b5967c8d9)
 Call ID: 35ccbf64-288f-4ec2-96f7-242b5967c8d9
  Args: