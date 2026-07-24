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
Angelica Margherita Edwina Hicks (born 16 September 1992) is a British fashion illustrator and internet personality.
As the great-granddaughter of Louis Mountbatten, 1st Earl Mountbatten of Burma, she is a relative of the British royal family and is included in the line of succession to the British throne.
Early life and family

Hicks was born on 16 September 1992 to Marina Allegra Federica Silvia Tondato, an Italian designer, and Ashley Louis David Hicks, a British artist and interior designer.
Hicks' paternal grandparents were the English interior decorator and designer David Nightingale Hicks and Lady Pamela Mountbatten, who served as a bridesmaid and as a lady-in-waiting to Elizabeth II.
Through her grandmother, Hicks is a relative of the Mountbatten family, itself a branch of the German princely Battenberg family, and a relative of the British royal family.
Hicks' great-grandparents, Louis Mountbatten, 1st Earl Mountbatten of Burma and The Honourable Edwina Ashley, served as the Viceroy and Vicereine of India.
She is a great-great-granddaughter of Prince Louis of Battenberg (later the 1st Marquess of Milford Haven) and Princess Victoria of Hesse and by Rhine, a granddaughter of Queen Victoria.
Hicks grew up in Chelsea, London and was educated at a boarding school.
Career

Hicks works as a visual artist and fashion illustrator.
Hicks also made commissioned pieces for the American fashion designer Tory Burch and illustrated for the magazines Elle and Porter.
In 2021, Hicks launched a TikTok channel where she parodies haute couture outfits from red carpet events and fashion shows, recreating them out of duct tape, trash bags, metallic wrappers, foil, candy, and other materials.
Her recreations included a Louis Vuitton tank dress worn by Emma Corrin on the cover of Vogue, which she made out of multigrain crackers, a Maison Schiaparelli couture cape that she made out of a white mattress cover, and Cagole boots by Balenciaga that she made out of duct tape.
By July 2022, Hicks amassed over 48,000 followers and her videos collectively received over 4 million likes.
Her videos led to Hicks collaborating with Valentino and Vogue Italia.
By September 2022, Hicks had over 86,000 followers on TikTok.
Personal life

Hicks resides in Carroll Gardens in Brooklyn, New York.



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
  AssignClass (154eb1b9-b3b7-4860-b87d-35b4122e89aa)
 Call ID: 154eb1b9-b3b7-4860-b87d-35b4122e89aa
  Args:
    source: Angelica_Margherita_Edwina_Hicks
    type: :Woman
  AssignClass (4b5925c9-0395-45ac-8ee6-72bd410a7d3c)
 Call ID: 4b5925c9-0395-45ac-8ee6-72bd410a7d3c
  Args:
    source: Angelica_Margherita_Edwina_Hicks
    type: :Person
  AddLiteral (257b8033-6e82-4dd0-87de-8c103c1db4ab)
 Call ID: 257b8033-6e82-4dd0-87de-8c103c1db4ab
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1992
    source: Angelica_Margherita_Edwina_Hicks
  AssignClass (6f00fe72-e158-4ade-958e-053b3eb05533)
 Call ID: 6f00fe72-e158-4ade-958e-053b3eb05533
  Args:
    type: :Woman
    source: Marina_Allegra_Federica_Silvia_Tondato
  AssignClass (9430f470-1843-49ab-b7c0-b0487f30b058)
 Call ID: 9430f470-1843-49ab-b7c0-b0487f30b058
  Args:
    type: :Person
    source: Marina_Allegra_Federica_Silvia_Tondato
  AssignClass (ae883568-a9c3-4c19-9a39-22bd5d094d84)
 Call ID: ae883568-a9c3-4c19-9a39-22bd5d094d84
  Args:
    type: :Man
    source: Ashley_Louis_David_Hicks
  AssignClass (664686c4-6872-44fe-819b-1e83b97aa4d3)
 Call ID: 664686c4-6872-44fe-819b-1e83b97aa4d3
  Args:
    source: Ashley_Louis_David_Hicks
    type: :Person
  AddTriple (938c26e8-d440-4ab9-b535-6a90a3c75b25)
 Call ID: 938c26e8-d440-4ab9-b535-6a90a3c75b25
  Args:
    relation: :hasMother
    target: Marina_Allegra_Federica_Silvia_Tondato
    source: Angelica_Margherita_Edwina_Hicks
  AddTriple (b4188c2b-87cc-4195-9d89-e51f276dcc5a)
 Call ID: b4188c2b-87cc-4195-9d89-e51f276dcc5a
  Args:
    source: Angelica_Margherita_Edwina_Hicks
    target: Ashley_Louis_David_Hicks
    relation: :hasFather
  AssignClass (4ddc8ad3-5e7b-46df-9242-d5cdd599f7a6)
 Call ID: 4ddc8ad3-5e7b-46df-9242-d5cdd599f7a6
  Args:
    type: :Man
    source: David_Nightingale_Hicks
  AssignClass (fd0ede76-aed6-4b27-a9c6-dc546c700989)
 Call ID: fd0ede76-aed6-4b27-a9c6-dc546c700989
  Args:
    type: :Person
    source: David_Nightingale_Hicks
  AssignClass (d090a21f-d648-4cdb-aecc-075915b10036)
 Call ID: d090a21f-d648-4cdb-aecc-075915b10036
  Args:
    source: Lady_Pamela_Mountbatten
    type: :Woman
  AssignClass (b2d65a74-1aef-484e-85fa-6da11d478c6a)
 Call ID: b2d65a74-1aef-484e-85fa-6da11d478c6a
  Args:
    type: :Person
    source: Lady_Pamela_Mountbatten
  AddTriple (41b79cd3-ef33-4c70-bf43-57b074371089)
 Call ID: 41b79cd3-ef33-4c70-bf43-57b074371089
  Args:
    relation: :hasFather
    target: David_Nightingale_Hicks
    source: Ashley_Louis_David_Hicks
  AddTriple (36608d6e-18ee-4c51-af11-bcb5d0ae78d8)
 Call ID: 36608d6e-18ee-4c51-af11-bcb5d0ae78d8
  Args:
    relation: :hasMother
    source: Ashley_Louis_David_Hicks
    target: Lady_Pamela_Mountbatten
  AssignClass (0bcf4e04-3efa-4334-9129-4b8d2262e697)
 Call ID: 0bcf4e04-3efa-4334-9129-4b8d2262e697
  Args:
    source: Louis_Mountbatten_1st_Earl_Mountbatten_of_Burma
    type: :Man
  AssignClass (bc94668c-6b8f-4de9-9f06-51ecab1fb278)
 Call ID: bc94668c-6b8f-4de9-9f06-51ecab1fb278
  Args:
    source: Louis_Mountbatten_1st_Earl_Mountbatten_of_Burma
    type: :Person
  AssignClass (edb21cb8-17b1-4feb-ba2f-e7f91a3ed839)
 Call ID: edb21cb8-17b1-4feb-ba2f-e7f91a3ed839
  Args:
    source: The_Honourable_Edwina_Ashley
    type: :Woman
  AssignClass (4effafc3-8b3d-44ca-b123-f2c42217200e)
 Call ID: 4effafc3-8b3d-44ca-b123-f2c42217200e
  Args:
    type: :Person
    source: The_Honourable_Edwina_Ashley
  AddTriple (e3676778-ae37-4046-85f3-7cb22e97a62e)
 Call ID: e3676778-ae37-4046-85f3-7cb22e97a62e
  Args:
    relation: :hasFather
    source: Lady_Pamela_Mountbatten
    target: Louis_Mountbatten_1st_Earl_Mountbatten_of_Burma
  AddTriple (a8fdf33b-f79f-4456-9ecc-94183e66a4ca)
 Call ID: a8fdf33b-f79f-4456-9ecc-94183e66a4ca
  Args:
    relation: :hasMother
    source: Lady_Pamela_Mountbatten
    target: The_Honourable_Edwina_Ashley
  AssignClass (4bb11009-c53c-44b1-9bd7-5360238b396a)
 Call ID: 4bb11009-c53c-44b1-9bd7-5360238b396a
  Args:
    type: :Man
    source: Prince_Louis_of_Battenberg
  AssignClass (2421372b-0ddd-41b1-bcb5-5fc7bd61a5a4)
 Call ID: 2421372b-0ddd-41b1-bcb5-5fc7bd61a5a4
  Args:
    type: :Person
    source: Prince_Louis_of_Battenberg
  AssignClass (a18716d3-c67d-4e54-9db3-21fab95f11cb)
 Call ID: a18716d3-c67d-4e54-9db3-21fab95f11cb
  Args:
    type: :Woman
    source: Princess_Victoria_of_Hesse_and_by_Rhine
  AssignClass (9b242c59-8ea8-4072-b9ce-50d51a891e30)
 Call ID: 9b242c59-8ea8-4072-b9ce-50d51a891e30
  Args:
    type: :Person
    source: Princess_Victoria_of_Hesse_and_by_Rhine
  AssignClass (92a41bc6-23b8-4db8-a228-0d429788f513)
 Call ID: 92a41bc6-23b8-4db8-a228-0d429788f513
  Args:
    source: Queen_Victoria
    type: :Woman
  AssignClass (ea711dcb-f892-4fbf-aeb8-add0b803f6e5)
 Call ID: ea711dcb-f892-4fbf-aeb8-add0b803f6e5
  Args:
    source: Queen_Victoria
    type: :Person
  AddTriple (4462baad-b5d5-4fd3-909d-8c9e296be628)
 Call ID: 4462baad-b5d5-4fd3-909d-8c9e296be628
  Args:
    source: Louis_Mountbatten_1st_Earl_Mountbatten_of_Burma
    target: Prince_Louis_of_Battenberg
    relation: :hasFather
  AddTriple (fbc5501b-b03f-4706-9b7c-b5095665ad3d)
 Call ID: fbc5501b-b03f-4706-9b7c-b5095665ad3d
  Args:
    relation: :hasMother
    target: Princess_Victoria_of_Hesse_and_by_Rhine
    source: Louis_Mountbatten_1st_Earl_Mountbatten_of_Burma
  AddTriple (a4b7d69c-efcb-4151-bd8b-f4b80845e9b7)
 Call ID: a4b7d69c-efcb-4151-bd8b-f4b80845e9b7
  Args:
    source: Princess_Victoria_of_Hesse_and_by_Rhine
    target: Queen_Victoria
    relation: :hasMother
  Finish (a261382b-cf2b-4619-90fc-4c7093c27449)
 Call ID: a261382b-cf2b-4619-90fc-4c7093c27449
  Args: