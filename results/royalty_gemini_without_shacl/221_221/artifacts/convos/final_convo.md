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
Anne Ferelith Fenella Bowes-Lyon (4 December 1917 – 26 September 1980), later styled Viscountess Anson and later Princess Anne of Denmark, was a British noblewoman and member of the Danish royal family by marriage, and a first cousin of Elizabeth II.
Born into the Bowes-Lyon family, she married Thomas Anson, Viscount Anson, and had two children, Patrick Anson, 5th Earl of Lichfield, and Lady Elizabeth Shakerley, before divorcing Anson in 1948.
She became a princess of Denmark by her second marriage to Prince Georg of Denmark in 1950.
Family

Anne Bowes-Lyon was born in Washington, D.C., in 1917.
John Herbert Bowes-Lyon and her mother was the Hon.
Fenella Hepburn-Stuart-Forbes-Trefusis, daughter of Charles Hepburn-Stuart-Forbes-Trefusis, 21st Baron Clinton.
Anne's paternal grandfather was Claude Bowes-Lyon, 14th
Earl of Strathmore and Kinghorne.
She was a niece of Queen Elizabeth the Queen Mother.
Anne had three younger sisters, two of whom were Nerissa and Katherine Bowes-Lyon, who were institutionalized in 1941 for severe intellectual disability.
Apart from early deceased Patricia (1916–1917), Nerissa (1919–1986) and Katherine (1926–2014), Anne also had one younger sister, Diana Cinderella Somervell (1923–1986).
Marriages

Anne married Lieutenant-Colonel Thomas William Arnold Anson (1913–1958) on 28 April 1938.
As her husband held the courtesy title of Viscount Anson, Anne was styled Viscountess Anson upon their marriage.
On 16 September 1950, at Glamis Castle, Anne, Viscountess Anson subsequently married Prince Georg of Denmark, upon which she became Her Highness Princess Anne of Denmark.
Death

Anne died in 1980, aged 62, in London of a heart attack.
She is buried alongside her second husband, Prince George of Denmark, at Bernstorffpark, Gentofte, Denmark.



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
  AssignClass (5db75eca-b207-424b-a3de-dce2ae660ea5)
 Call ID: 5db75eca-b207-424b-a3de-dce2ae660ea5
  Args:
    source: :Anne_Bowes-Lyon
    type: :Woman
  AssignClass (a4f28b95-7ac5-4a1d-a4d3-ed7da4f899fe)
 Call ID: a4f28b95-7ac5-4a1d-a4d3-ed7da4f899fe
  Args:
    type: :Person
    source: :Anne_Bowes-Lyon
  AddLiteral (f07824f2-07a4-4d92-b535-27a866c66264)
 Call ID: f07824f2-07a4-4d92-b535-27a866c66264
  Args:
    source: :Anne_Bowes-Lyon
    literal_value: 1917
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (20cc3ad5-2764-4eea-9e28-cd1be462d8d5)
 Call ID: 20cc3ad5-2764-4eea-9e28-cd1be462d8d5
  Args:
    relation: :hasDeathYear
    source: :Anne_Bowes-Lyon
    literal_value: 1980
    literal_type: xsd:integer
  AssignClass (62f5df74-1d14-422e-9f57-e323cc8d241b)
 Call ID: 62f5df74-1d14-422e-9f57-e323cc8d241b
  Args:
    source: :John_Herbert_Bowes-Lyon
    type: :Man
  AssignClass (86dc0d14-95d1-4a0c-9aba-38a65910ad51)
 Call ID: 86dc0d14-95d1-4a0c-9aba-38a65910ad51
  Args:
    source: :John_Herbert_Bowes-Lyon
    type: :Person
  AddTriple (a49ac354-24c6-4ce0-b813-c29df07ab21a)
 Call ID: a49ac354-24c6-4ce0-b813-c29df07ab21a
  Args:
    target: :John_Herbert_Bowes-Lyon
    source: :Anne_Bowes-Lyon
    relation: :hasFather
  AssignClass (8a0629d0-9276-4e52-b023-dbd861493d65)
 Call ID: 8a0629d0-9276-4e52-b023-dbd861493d65
  Args:
    type: :Woman
    source: :Fenella_Hepburn-Stuart-Forbes-Trefusis
  AssignClass (30ad1135-6970-47fa-bdd8-9cf17e719295)
 Call ID: 30ad1135-6970-47fa-bdd8-9cf17e719295
  Args:
    type: :Person
    source: :Fenella_Hepburn-Stuart-Forbes-Trefusis
  AddTriple (7eeca52e-befc-409e-806b-505f3c23494e)
 Call ID: 7eeca52e-befc-409e-806b-505f3c23494e
  Args:
    target: :Fenella_Hepburn-Stuart-Forbes-Trefusis
    source: :Anne_Bowes-Lyon
    relation: :hasMother
  AssignClass (86a2ca27-3630-4080-9556-b7169360de36)
 Call ID: 86a2ca27-3630-4080-9556-b7169360de36
  Args:
    source: :Charles_Hepburn-Stuart-Forbes-Trefusis
    type: :Man
  AssignClass (2430cbbe-65b7-440b-b07b-6c4035ebdde4)
 Call ID: 2430cbbe-65b7-440b-b07b-6c4035ebdde4
  Args:
    type: :Person
    source: :Charles_Hepburn-Stuart-Forbes-Trefusis
  AddTriple (c73275a6-8d64-461e-85ea-26a331d679e0)
 Call ID: c73275a6-8d64-461e-85ea-26a331d679e0
  Args:
    target: :Charles_Hepburn-Stuart-Forbes-Trefusis
    source: :Fenella_Hepburn-Stuart-Forbes-Trefusis
    relation: :hasFather
  AssignClass (69ed0ef6-cbb6-43c3-a5a9-58c51d435070)
 Call ID: 69ed0ef6-cbb6-43c3-a5a9-58c51d435070
  Args:
    source: :Claude_Bowes-Lyon
    type: :Man
  AssignClass (85c8bbe6-b761-4537-b986-11ea54de16f1)
 Call ID: 85c8bbe6-b761-4537-b986-11ea54de16f1
  Args:
    type: :Person
    source: :Claude_Bowes-Lyon
  AddTriple (6369bef2-bedc-4daa-8c74-9378d97455de)
 Call ID: 6369bef2-bedc-4daa-8c74-9378d97455de
  Args:
    source: :John_Herbert_Bowes-Lyon
    target: :Claude_Bowes-Lyon
    relation: :hasFather
  AssignClass (4d695e83-ebaa-4158-835c-709e10083094)
 Call ID: 4d695e83-ebaa-4158-835c-709e10083094
  Args:
    source: :Thomas_Anson
    type: :Man
  AssignClass (6bdfed77-4938-4061-bb72-55fe34dfceb1)
 Call ID: 6bdfed77-4938-4061-bb72-55fe34dfceb1
  Args:
    type: :Person
    source: :Thomas_Anson
  AddLiteral (fa0bf73f-43dc-462c-ae02-b97f19c0c30e)
 Call ID: fa0bf73f-43dc-462c-ae02-b97f19c0c30e
  Args:
    literal_type: xsd:integer
    source: :Anne_Bowes-Lyon
    literal_value: 1938
    relation: :hasMarriageYear
  AddTriple (ae350aa1-c188-4471-aa83-b935fe9ad81b)
 Call ID: ae350aa1-c188-4471-aa83-b935fe9ad81b
  Args:
    source: :Anne_Bowes-Lyon
    target: :Thomas_Anson
    relation: :hasRelation
  AssignClass (e5988ccc-5381-412e-a782-e00114b3fd01)
 Call ID: e5988ccc-5381-412e-a782-e00114b3fd01
  Args:
    source: :Patrick_Anson
    type: :Man
  AssignClass (7dd89762-7dc8-4847-ac33-f7b2aeab61a9)
 Call ID: 7dd89762-7dc8-4847-ac33-f7b2aeab61a9
  Args:
    type: :Person
    source: :Patrick_Anson
  AddTriple (308e847b-8e11-4f54-9c6e-ec9c355fd37c)
 Call ID: 308e847b-8e11-4f54-9c6e-ec9c355fd37c
  Args:
    source: :Patrick_Anson
    target: :Anne_Bowes-Lyon
    relation: :isChildOf
  AddTriple (239322d1-1eaf-4aa5-aff1-5d5425e3334c)
 Call ID: 239322d1-1eaf-4aa5-aff1-5d5425e3334c
  Args:
    relation: :isChildOf
    target: :Thomas_Anson
    source: :Patrick_Anson
  AssignClass (6c57ff0c-b3f9-46f0-87ba-8fd144710815)
 Call ID: 6c57ff0c-b3f9-46f0-87ba-8fd144710815
  Args:
    type: :Woman
    source: :Elizabeth_Shakerley
  AssignClass (a4b6991b-810e-46b2-8e2d-aa64d23a9341)
 Call ID: a4b6991b-810e-46b2-8e2d-aa64d23a9341
  Args:
    source: :Elizabeth_Shakerley
    type: :Person
  AddTriple (54dc12cb-b144-47d3-b87d-8e0d875f39f7)
 Call ID: 54dc12cb-b144-47d3-b87d-8e0d875f39f7
  Args:
    relation: :isChildOf
    source: :Elizabeth_Shakerley
    target: :Anne_Bowes-Lyon
  AddTriple (62099b7c-7e46-434d-8ce5-c8ee22b14929)
 Call ID: 62099b7c-7e46-434d-8ce5-c8ee22b14929
  Args:
    relation: :isChildOf
    source: :Elizabeth_Shakerley
    target: :Thomas_Anson
  AssignClass (de7dc971-8949-448b-bf6a-8c7d31935967)
 Call ID: de7dc971-8949-448b-bf6a-8c7d31935967
  Args:
    source: :Prince_Georg_of_Denmark
    type: :Man
  AssignClass (ff724e07-d151-41f5-9d99-ea22a9a4c5e7)
 Call ID: ff724e07-d151-41f5-9d99-ea22a9a4c5e7
  Args:
    source: :Prince_Georg_of_Denmark
    type: :Person
  AddLiteral (8dfae77a-9fc8-486d-ad0b-09ae852599f8)
 Call ID: 8dfae77a-9fc8-486d-ad0b-09ae852599f8
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1950
    source: :Anne_Bowes-Lyon
  AddTriple (a51abecb-fbee-40a1-8e77-4e5349596737)
 Call ID: a51abecb-fbee-40a1-8e77-4e5349596737
  Args:
    relation: :hasRelation
    target: :Prince_Georg_of_Denmark
    source: :Anne_Bowes-Lyon
  AssignClass (0c571128-520e-45c5-91fb-8288d4eb48e6)
 Call ID: 0c571128-520e-45c5-91fb-8288d4eb48e6
  Args:
    source: :Patricia_Bowes-Lyon
    type: :Woman
  AssignClass (da818fbf-0004-4245-a4e2-aebcf57f91fe)
 Call ID: da818fbf-0004-4245-a4e2-aebcf57f91fe
  Args:
    source: :Patricia_Bowes-Lyon
    type: :Person
  AddTriple (cfc99f02-cbf3-48ca-ba7f-b88be95855e1)
 Call ID: cfc99f02-cbf3-48ca-ba7f-b88be95855e1
  Args:
    relation: :isSiblingOf
    target: :Patricia_Bowes-Lyon
    source: :Anne_Bowes-Lyon
  AssignClass (4a114b95-56a2-4db8-bb65-56171306bddb)
 Call ID: 4a114b95-56a2-4db8-bb65-56171306bddb
  Args:
    type: :Woman
    source: :Nerissa_Bowes-Lyon
  AssignClass (bb525be6-9843-47bb-8d24-b7ffeef8b199)
 Call ID: bb525be6-9843-47bb-8d24-b7ffeef8b199
  Args:
    type: :Person
    source: :Nerissa_Bowes-Lyon
  AddTriple (2b3dd9a0-5f04-45da-9b15-17a3b9bf6f73)
 Call ID: 2b3dd9a0-5f04-45da-9b15-17a3b9bf6f73
  Args:
    source: :Anne_Bowes-Lyon
    target: :Nerissa_Bowes-Lyon
    relation: :isSiblingOf
  AssignClass (5f63f4f1-9cf8-46c7-8991-df56c4af8e86)
 Call ID: 5f63f4f1-9cf8-46c7-8991-df56c4af8e86
  Args:
    type: :Woman
    source: :Katherine_Bowes-Lyon
  AssignClass (ccc2c743-ff57-4f0d-8e04-53302ec3fa1e)
 Call ID: ccc2c743-ff57-4f0d-8e04-53302ec3fa1e
  Args:
    type: :Person
    source: :Katherine_Bowes-Lyon
  AddTriple (b15bb26d-481f-4571-8d94-ec215be1057d)
 Call ID: b15bb26d-481f-4571-8d94-ec215be1057d
  Args:
    source: :Anne_Bowes-Lyon
    target: :Katherine_Bowes-Lyon
    relation: :isSiblingOf
  AssignClass (64eeeada-5cd9-4501-8fd8-2aa55a61613f)
 Call ID: 64eeeada-5cd9-4501-8fd8-2aa55a61613f
  Args:
    type: :Woman
    source: :Diana_Cinderella_Somervell
  AssignClass (057a00bc-4316-4747-bc0b-f742ee6c2f6e)
 Call ID: 057a00bc-4316-4747-bc0b-f742ee6c2f6e
  Args:
    type: :Person
    source: :Diana_Cinderella_Somervell
  AddTriple (8f6d4db9-e8ff-4de7-95e5-20bcfc230fdd)
 Call ID: 8f6d4db9-e8ff-4de7-95e5-20bcfc230fdd
  Args:
    relation: :isSiblingOf
    source: :Anne_Bowes-Lyon
    target: :Diana_Cinderella_Somervell
  Finish (47b66c15-a81c-4ec3-aec7-63c25c068d43)
 Call ID: 47b66c15-a81c-4ec3-aec7-63c25c068d43
  Args: