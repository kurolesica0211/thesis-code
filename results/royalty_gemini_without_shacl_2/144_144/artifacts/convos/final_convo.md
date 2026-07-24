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
  AssignClass (97603632-8378-44e1-8e64-2948d005fc3f)
 Call ID: 97603632-8378-44e1-8e64-2948d005fc3f
  Args:
    source: Prince_Christoph_of_Hesse
    type: :Man
  AssignClass (06bcb4dc-aff0-424b-ac28-e2c9e6eae44a)
 Call ID: 06bcb4dc-aff0-424b-ac28-e2c9e6eae44a
  Args:
    source: Prince_Christoph_of_Hesse
    type: :Person
  AddLiteral (b8fb7548-b23a-44e4-8d88-936558f62265)
 Call ID: b8fb7548-b23a-44e4-8d88-936558f62265
  Args:
    literal_value: 1901
    relation: :hasBirthYear
    source: Prince_Christoph_of_Hesse
    literal_type: xsd:integer
  AddLiteral (06ea6e4b-aed5-418a-9cb0-2ce8acd34688)
 Call ID: 06ea6e4b-aed5-418a-9cb0-2ce8acd34688
  Args:
    literal_value: 1943
    source: Prince_Christoph_of_Hesse
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (4851baac-eef1-4713-9ad4-3da8f51532b3)
 Call ID: 4851baac-eef1-4713-9ad4-3da8f51532b3
  Args:
    source: Kaiser_Wilhelm_II
    type: :Man
  AssignClass (cd3a8743-1d6f-4838-9368-0423d85ec123)
 Call ID: cd3a8743-1d6f-4838-9368-0423d85ec123
  Args:
    type: :Person
    source: Kaiser_Wilhelm_II
  AddTriple (ed823dbf-1376-47e8-824d-0dd61c6a6579)
 Call ID: ed823dbf-1376-47e8-824d-0dd61c6a6579
  Args:
    source: Prince_Christoph_of_Hesse
    relation: :hasRelation
    target: Kaiser_Wilhelm_II
  AssignClass (bc04f171-ab2f-4429-884e-101b295ec1c0)
 Call ID: bc04f171-ab2f-4429-884e-101b295ec1c0
  Args:
    source: Prince_Philip_of_Greece_and_Denmark
    type: :Man
  AssignClass (f7d9e2a2-4e75-4ba5-b42d-7be058edd146)
 Call ID: f7d9e2a2-4e75-4ba5-b42d-7be058edd146
  Args:
    type: :Person
    source: Prince_Philip_of_Greece_and_Denmark
  AssignClass (25ec6de8-0bb1-4ca1-9b56-71fc08d1597e)
 Call ID: 25ec6de8-0bb1-4ca1-9b56-71fc08d1597e
  Args:
    type: :Woman
    source: Queen_Elizabeth_II
  AssignClass (7560fd13-449c-4657-bc33-cd68d0975e41)
 Call ID: 7560fd13-449c-4657-bc33-cd68d0975e41
  Args:
    type: :Person
    source: Queen_Elizabeth_II
  AddTriple (a1ea3f32-93f8-4470-a40d-6ec5beb87f65)
 Call ID: a1ea3f32-93f8-4470-a40d-6ec5beb87f65
  Args:
    source: Prince_Philip_of_Greece_and_Denmark
    relation: :hasRelation
    target: Queen_Elizabeth_II
  AssignClass (3241b8d7-3fa5-4a51-b1dd-b13a2f217a47)
 Call ID: 3241b8d7-3fa5-4a51-b1dd-b13a2f217a47
  Args:
    type: :Man
    source: Prince_Frederick_Charles_of_Hesse
  AssignClass (177fbc48-f0d0-42ee-a0ec-408ab45e3846)
 Call ID: 177fbc48-f0d0-42ee-a0ec-408ab45e3846
  Args:
    type: :Person
    source: Prince_Frederick_Charles_of_Hesse
  AssignClass (96b7e985-d621-46ba-8b2e-0ec5c4cd8226)
 Call ID: 96b7e985-d621-46ba-8b2e-0ec5c4cd8226
  Args:
    type: :Woman
    source: Princess_Margaret_of_Prussia
  AssignClass (840f0644-f9a1-45e1-8da6-ac03bec8ebea)
 Call ID: 840f0644-f9a1-45e1-8da6-ac03bec8ebea
  Args:
    type: :Person
    source: Princess_Margaret_of_Prussia
  AddTriple (658d1d3e-2745-45af-af6a-587f16f77600)
 Call ID: 658d1d3e-2745-45af-af6a-587f16f77600
  Args:
    target: Prince_Frederick_Charles_of_Hesse
    relation: :hasFather
    source: Prince_Christoph_of_Hesse
  AddTriple (9e9020ba-5684-4871-8bc7-8698dc9d40bf)
 Call ID: 9e9020ba-5684-4871-8bc7-8698dc9d40bf
  Args:
    target: Princess_Margaret_of_Prussia
    source: Prince_Christoph_of_Hesse
    relation: :hasMother
  AssignClass (fcb02233-46ea-4caa-ae66-800af2d9bdcd)
 Call ID: fcb02233-46ea-4caa-ae66-800af2d9bdcd
  Args:
    source: Prince_Richard_of_Hesse
    type: :Man
  AssignClass (48bff550-44a5-404a-b597-913b788b6901)
 Call ID: 48bff550-44a5-404a-b597-913b788b6901
  Args:
    type: :Person
    source: Prince_Richard_of_Hesse
  AddTriple (e4989128-386b-4182-affa-2bdf926e4498)
 Call ID: e4989128-386b-4182-affa-2bdf926e4498
  Args:
    target: Prince_Richard_of_Hesse
    relation: :isSiblingOf
    source: Prince_Christoph_of_Hesse
  AssignClass (324285c1-8f69-466a-8ae3-38a60503e95b)
 Call ID: 324285c1-8f69-466a-8ae3-38a60503e95b
  Args:
    type: :Man
    source: Emperor_Frederick_III
  AssignClass (7db59a64-b5e2-4991-a5e2-07ba0f779c15)
 Call ID: 7db59a64-b5e2-4991-a5e2-07ba0f779c15
  Args:
    source: Emperor_Frederick_III
    type: :Person
  AssignClass (abeceef0-59f1-4ba5-8dd9-9bea08846e66)
 Call ID: abeceef0-59f1-4ba5-8dd9-9bea08846e66
  Args:
    source: Victoria_Princess_Royal
    type: :Woman
  AssignClass (00a04181-1576-4af0-b2d7-c1734372ac8f)
 Call ID: 00a04181-1576-4af0-b2d7-c1734372ac8f
  Args:
    source: Victoria_Princess_Royal
    type: :Person
  AddTriple (8d888c05-36cf-425a-a2f4-e6505f29e59f)
 Call ID: 8d888c05-36cf-425a-a2f4-e6505f29e59f
  Args:
    relation: :hasFather
    source: Princess_Margaret_of_Prussia
    target: Emperor_Frederick_III
  AddTriple (9cecd4f8-2484-4ba8-8c11-149b1be86b7d)
 Call ID: 9cecd4f8-2484-4ba8-8c11-149b1be86b7d
  Args:
    relation: :hasMother
    source: Princess_Margaret_of_Prussia
    target: Victoria_Princess_Royal
  AssignClass (c7286f7f-cc33-4c0d-978a-660a362f72a0)
 Call ID: c7286f7f-cc33-4c0d-978a-660a362f72a0
  Args:
    type: :Woman
    source: Queen_Victoria
  AssignClass (affbf198-6ff9-45b8-9a29-ba5c2999b235)
 Call ID: affbf198-6ff9-45b8-9a29-ba5c2999b235
  Args:
    type: :Person
    source: Queen_Victoria
  AssignClass (1d060962-a452-44b9-8dff-d4e70f828dea)
 Call ID: 1d060962-a452-44b9-8dff-d4e70f828dea
  Args:
    source: Prince_Albert_of_Saxe-Coburg_and_Gotha
    type: :Man
  AssignClass (fc341eb9-c874-41d0-8974-acdd143b33c5)
 Call ID: fc341eb9-c874-41d0-8974-acdd143b33c5
  Args:
    type: :Person
    source: Prince_Albert_of_Saxe-Coburg_and_Gotha
  AssignClass (365a8c27-1424-49d3-88f1-c4c47e9b79c8)
 Call ID: 365a8c27-1424-49d3-88f1-c4c47e9b79c8
  Args:
    source: Prince_Philipp_of_Hesse
    type: :Man
  AssignClass (e53d4881-134d-4408-9236-d1263181f4bc)
 Call ID: e53d4881-134d-4408-9236-d1263181f4bc
  Args:
    source: Prince_Philipp_of_Hesse
    type: :Person
  AssignClass (8e4c1206-d1ca-4cbd-ac28-4613665008d0)
 Call ID: 8e4c1206-d1ca-4cbd-ac28-4613665008d0
  Args:
    source: Prince_Wolfgang_of_Hesse
    type: :Man
  AssignClass (1bffefdd-5004-4e7b-823d-50422434d076)
 Call ID: 1bffefdd-5004-4e7b-823d-50422434d076
  Args:
    type: :Person
    source: Prince_Wolfgang_of_Hesse
  AssignClass (eeb21e81-bb72-4aa5-848f-a5227e3dcc3c)
 Call ID: eeb21e81-bb72-4aa5-848f-a5227e3dcc3c
  Args:
    source: Friedrich_Wilhelm_of_Hesse
    type: :Man
  AssignClass (5d1f4747-1b5d-42f0-b635-f4dd5259488a)
 Call ID: 5d1f4747-1b5d-42f0-b635-f4dd5259488a
  Args:
    type: :Person
    source: Friedrich_Wilhelm_of_Hesse
  AssignClass (f08f29b4-57f4-420c-889c-82b415023533)
 Call ID: f08f29b4-57f4-420c-889c-82b415023533
  Args:
    type: :Man
    source: Maximilian_of_Hesse
  AssignClass (ea9f7799-f7da-49b5-8190-7edff1c567d2)
 Call ID: ea9f7799-f7da-49b5-8190-7edff1c567d2
  Args:
    type: :Person
    source: Maximilian_of_Hesse
  AddTriple (123521bb-69d6-440d-9d58-2980c3b5ad5f)
 Call ID: 123521bb-69d6-440d-9d58-2980c3b5ad5f
  Args:
    target: Prince_Philipp_of_Hesse
    source: Prince_Christoph_of_Hesse
    relation: :isSiblingOf
  AddTriple (84aaa931-eb7f-40aa-9785-b3daf33aee7f)
 Call ID: 84aaa931-eb7f-40aa-9785-b3daf33aee7f
  Args:
    target: Prince_Wolfgang_of_Hesse
    relation: :isSiblingOf
    source: Prince_Christoph_of_Hesse
  AddTriple (36651ae9-e725-4124-88fe-27d4757d0ade)
 Call ID: 36651ae9-e725-4124-88fe-27d4757d0ade
  Args:
    target: Friedrich_Wilhelm_of_Hesse
    source: Prince_Christoph_of_Hesse
    relation: :isSiblingOf
  AddTriple (ecbbfc8d-ed71-46ab-9702-1b617f35970f)
 Call ID: ecbbfc8d-ed71-46ab-9702-1b617f35970f
  Args:
    target: Maximilian_of_Hesse
    source: Prince_Christoph_of_Hesse
    relation: :isSiblingOf
  AssignClass (45547893-a3b7-49a3-b374-41d55f185f0f)
 Call ID: 45547893-a3b7-49a3-b374-41d55f185f0f
  Args:
    source: Princess_Sophie_of_Greece_and_Denmark
    type: :Woman
  AssignClass (a4cd7c6f-da5c-4966-a7a2-385294897ad2)
 Call ID: a4cd7c6f-da5c-4966-a7a2-385294897ad2
  Args:
    type: :Person
    source: Princess_Sophie_of_Greece_and_Denmark
  AddTriple (8bd915ca-ed7f-4512-8d0d-70c12a492cc7)
 Call ID: 8bd915ca-ed7f-4512-8d0d-70c12a492cc7
  Args:
    relation: :hasRelation
    source: Prince_Christoph_of_Hesse
    target: Princess_Sophie_of_Greece_and_Denmark
  AddLiteral (cd0b0d98-96e2-4fde-9400-22c5d8671722)
 Call ID: cd0b0d98-96e2-4fde-9400-22c5d8671722
  Args:
    literal_value: 1930
    relation: :hasMarriageYear
    source: Prince_Christoph_of_Hesse
    literal_type: xsd:integer
  AssignClass (14802311-88a9-46b1-8c10-85d91f44fa91)
 Call ID: 14802311-88a9-46b1-8c10-85d91f44fa91
  Args:
    type: :Man
    source: Prince_Andrew_of_Greece_and_Denmark
  AssignClass (b9978ebb-9a32-459f-93c0-be80e32b1854)
 Call ID: b9978ebb-9a32-459f-93c0-be80e32b1854
  Args:
    source: Prince_Andrew_of_Greece_and_Denmark
    type: :Person
  AssignClass (ed31f907-1281-4859-8f38-efca981a96eb)
 Call ID: ed31f907-1281-4859-8f38-efca981a96eb
  Args:
    type: :Woman
    source: Princess_Alice_of_Battenberg
  AssignClass (218249fc-1e49-40ec-8509-56423316a9b1)
 Call ID: 218249fc-1e49-40ec-8509-56423316a9b1
  Args:
    source: Princess_Alice_of_Battenberg
    type: :Person
  AddTriple (e1c062e9-5dde-4a65-a546-2d91656e34ce)
 Call ID: e1c062e9-5dde-4a65-a546-2d91656e34ce
  Args:
    target: Prince_Andrew_of_Greece_and_Denmark
    relation: :hasFather
    source: Princess_Sophie_of_Greece_and_Denmark
  AddTriple (4cd03725-90f2-46c7-8984-a3334a3ed2b5)
 Call ID: 4cd03725-90f2-46c7-8984-a3334a3ed2b5
  Args:
    relation: :hasMother
    source: Princess_Sophie_of_Greece_and_Denmark
    target: Princess_Alice_of_Battenberg
  AddTriple (9c980c5f-8b12-4e9b-b468-601772bb878b)
 Call ID: 9c980c5f-8b12-4e9b-b468-601772bb878b
  Args:
    source: Princess_Sophie_of_Greece_and_Denmark
    relation: :isSiblingOf
    target: Prince_Philip_of_Greece_and_Denmark
  AssignClass (81adcbc6-0c53-4e31-9637-b6c9498b35c7)
 Call ID: 81adcbc6-0c53-4e31-9637-b6c9498b35c7
  Args:
    type: :Man
    source: Prince_George_William_of_Hanover
  AssignClass (e6e4507c-55ab-46c2-82f6-cfd5a3857d88)
 Call ID: e6e4507c-55ab-46c2-82f6-cfd5a3857d88
  Args:
    source: Prince_George_William_of_Hanover
    type: :Person
  AddTriple (b4b940e1-9df2-4184-be35-df4153bda9a9)
 Call ID: b4b940e1-9df2-4184-be35-df4153bda9a9
  Args:
    target: Prince_George_William_of_Hanover
    source: Princess_Sophie_of_Greece_and_Denmark
    relation: :hasRelation
  AssignClass (51e26e50-0051-4cb1-b568-fb2da9d93289)
 Call ID: 51e26e50-0051-4cb1-b568-fb2da9d93289
  Args:
    type: :Woman
    source: Queen_Fredrica_of_Greece
  AssignClass (7f69296b-0493-45e7-ae53-f0f2e3a5a89b)
 Call ID: 7f69296b-0493-45e7-ae53-f0f2e3a5a89b
  Args:
    type: :Person
    source: Queen_Fredrica_of_Greece
  AddTriple (2532d5e8-74c2-44f4-ab0d-1dc853242ba0)
 Call ID: 2532d5e8-74c2-44f4-ab0d-1dc853242ba0
  Args:
    source: Prince_George_William_of_Hanover
    relation: :isSiblingOf
    target: Queen_Fredrica_of_Greece
  AssignClass (c71aaab7-7086-478e-ae04-16871b2cb25d)
 Call ID: c71aaab7-7086-478e-ae04-16871b2cb25d
  Args:
    source: King_Charles_III
    type: :Man
  AssignClass (ce504962-9954-4190-8ad9-65427b3e29e4)
 Call ID: ce504962-9954-4190-8ad9-65427b3e29e4
  Args:
    source: King_Charles_III
    type: :Person
  Finish (15cdd3ed-03b2-4c08-9227-bb7279fa88d3)
 Call ID: 15cdd3ed-03b2-4c08-9227-bb7279fa88d3
  Args: