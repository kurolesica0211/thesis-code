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
Princess Nuria


Princess Françoise


Princess Mariam


Princess Monique


Prince Juan Jorge de Bagration-Mukhrani (born 18 August 1977) is a Spanish-born Georgian prince and member of the House of Mukhrani of the Bagrationi dynasty and a distant relation to the Spanish royal family.
Early life and family

Prince Juan Jorge de Bagration-Mukhrani was born on 18 August 1977 in Madrid to Prince Bagrat de Bagration y de Baviera and Doña María del Carmen de Ulloa y Suelves.
His paternal grandfather, Prince Irakli Bagration of Mukhrani, was exiled from Georgia during the invasion of the Red Army, living in Germany, Italy, and finally settling in Spain.
His paternal grandmother, Infanta María de las Mercedes of Spain was a member of the Spanish royal family and the German House of Wittelsbach; she was the daughter of Prince Ferdinand of Bavaria, granddaughter of Alfonso XII of Spain, and niece of Alfonso XIII of Spain.
His maternal grandfather was Gonzalo Maria de Ulloa y Ramírez de Haro, Marqués de Castro-Serna, Count de Adanero.
Prince Juan's parents divorced in 2005 and his father remarried in 2009 to Françoise Cazaudehore.
Prince Juan is a member of the House of Mukhrani, a branch of the Bagrationi dynasty that ruled Georgia from the Middle Ages until the nineteenth century, when Georgia was annexed into the Russian Empire.
Prince Juan studied at Collège Alpin International Beau Soleil, a boarding school in Villars-sur-Ollon, Switzerland and was a schoolmate and childhood friend of Cayetano Rivera Ordóñez.
Personal life

Prince Juan met Kristine Dzidziguri, a Georgian model, in 2014.
They were married a few months later in a civil ceremony on 10 May 2014 in Ronda, Spain.
The couple began planning a religious ceremony but were delayed due to social and political conflicts within Georgia and because of Prince Juan's father's declining health.
On 2 June 2018, Prince Juan and Dzidziguri received a blessing from Ilia II of Georgia, the Catholicos-Patriarch of All Georgia.
Their wedding reception was held at the Palace of Mukhrani.
Later during their Indonesian tour, Prince Juan and Princess Kristine attended a gala lunch focused on establishing a cultural relationship between Indonesia and Georgia.
Prince Juan is the founder of the Georgian Foundation, a non-profit organization that promotes Georgian culture.
In October 2019 he launched a wine brand called Prince Ioane Bagrationi wines.



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
  AssignClass (0256d212-4462-4a3d-b6e3-651a158051a3)
 Call ID: 0256d212-4462-4a3d-b6e3-651a158051a3
  Args:
    type: :Man
    source: Prince_Juan_Jorge_de_Bagration-Mukhrani
  AssignClass (461c967e-6a39-4ddc-94aa-a35f49465e4f)
 Call ID: 461c967e-6a39-4ddc-94aa-a35f49465e4f
  Args:
    type: :Person
    source: Prince_Juan_Jorge_de_Bagration-Mukhrani
  AddLiteral (a5b38708-3a91-4ebf-a41a-f1bda425091f)
 Call ID: a5b38708-3a91-4ebf-a41a-f1bda425091f
  Args:
    source: Prince_Juan_Jorge_de_Bagration-Mukhrani
    literal_value: 1977
    relation: :hasBirthYear
    literal_type: xsd:integer
  AssignClass (6ded88c3-4c4e-4aa4-a199-bd667646019b)
 Call ID: 6ded88c3-4c4e-4aa4-a199-bd667646019b
  Args:
    type: :Man
    source: Prince_Bagrat_de_Bagration_y_de_Baviera
  AssignClass (9a246966-7c85-433b-a863-db57fc675373)
 Call ID: 9a246966-7c85-433b-a863-db57fc675373
  Args:
    type: :Person
    source: Prince_Bagrat_de_Bagration_y_de_Baviera
  AddTriple (86dc517f-6d27-48e0-ab08-28001f5f3e39)
 Call ID: 86dc517f-6d27-48e0-ab08-28001f5f3e39
  Args:
    source: Prince_Juan_Jorge_de_Bagration-Mukhrani
    target: Prince_Bagrat_de_Bagration_y_de_Baviera
    relation: :hasFather
  AssignClass (eda72816-825e-4264-8485-468b865e9279)
 Call ID: eda72816-825e-4264-8485-468b865e9279
  Args:
    type: :Woman
    source: Dona_Maria_del_Carmen_de_Ulloa_y_Suelves
  AssignClass (fcc3ed9b-ee02-49d7-b47c-337e13dce558)
 Call ID: fcc3ed9b-ee02-49d7-b47c-337e13dce558
  Args:
    source: Dona_Maria_del_Carmen_de_Ulloa_y_Suelves
    type: :Person
  AddTriple (ba8d65c2-a26d-4f6a-97d4-924e6a02df9e)
 Call ID: ba8d65c2-a26d-4f6a-97d4-924e6a02df9e
  Args:
    target: Dona_Maria_del_Carmen_de_Ulloa_y_Suelves
    relation: :hasMother
    source: Prince_Juan_Jorge_de_Bagration-Mukhrani
  AssignClass (f00cb9b9-e3a8-4097-b7ee-db1bca7e1540)
 Call ID: f00cb9b9-e3a8-4097-b7ee-db1bca7e1540
  Args:
    type: :Man
    source: Prince_Irakli_Bagration_of_Mukhrani
  AssignClass (ab3f5979-f2d8-44d3-b9e7-2cda2ec273b3)
 Call ID: ab3f5979-f2d8-44d3-b9e7-2cda2ec273b3
  Args:
    source: Prince_Irakli_Bagration_of_Mukhrani
    type: :Person
  AddTriple (b172a798-1d9a-488d-ac6f-994c47dc4652)
 Call ID: b172a798-1d9a-488d-ac6f-994c47dc4652
  Args:
    source: Prince_Bagrat_de_Bagration_y_de_Baviera
    target: Prince_Irakli_Bagration_of_Mukhrani
    relation: :hasFather
  AssignClass (df0827e2-92a3-48e0-9a17-e5f2a63fa428)
 Call ID: df0827e2-92a3-48e0-9a17-e5f2a63fa428
  Args:
    source: Infanta_Maria_de_las_Mercedes_of_Spain
    type: :Woman
  AssignClass (5d7f2319-6bb0-4d5c-9b86-f0ffd093d079)
 Call ID: 5d7f2319-6bb0-4d5c-9b86-f0ffd093d079
  Args:
    source: Infanta_Maria_de_las_Mercedes_of_Spain
    type: :Person
  AddTriple (9ccd5e3e-29f3-4118-9f5f-899fc25aea3d)
 Call ID: 9ccd5e3e-29f3-4118-9f5f-899fc25aea3d
  Args:
    relation: :hasMother
    target: Infanta_Maria_de_las_Mercedes_of_Spain
    source: Prince_Bagrat_de_Bagration_y_de_Baviera
  AssignClass (6fa48010-2f42-4921-8b96-a1e0b9bdb6b7)
 Call ID: 6fa48010-2f42-4921-8b96-a1e0b9bdb6b7
  Args:
    source: Prince_Ferdinand_of_Bavaria
    type: :Man
  AssignClass (58fad088-3bec-497d-944b-cf7fdc787cb5)
 Call ID: 58fad088-3bec-497d-944b-cf7fdc787cb5
  Args:
    type: :Person
    source: Prince_Ferdinand_of_Bavaria
  AddTriple (16b26e7d-f5f9-4b24-82a2-2922dedc0107)
 Call ID: 16b26e7d-f5f9-4b24-82a2-2922dedc0107
  Args:
    source: Infanta_Maria_de_las_Mercedes_of_Spain
    relation: :hasFather
    target: Prince_Ferdinand_of_Bavaria
  AssignClass (ad939a3f-9803-4ad2-93aa-8fdf52f46c66)
 Call ID: ad939a3f-9803-4ad2-93aa-8fdf52f46c66
  Args:
    type: :Man
    source: Alfonso_XII_of_Spain
  AssignClass (1ed4d716-8f7b-4a0d-8195-297766bf7215)
 Call ID: 1ed4d716-8f7b-4a0d-8195-297766bf7215
  Args:
    type: :Person
    source: Alfonso_XII_of_Spain
  AssignClass (ac5424b6-9023-472a-a501-7f4a87559e06)
 Call ID: ac5424b6-9023-472a-a501-7f4a87559e06
  Args:
    type: :Man
    source: Gonzalo_Maria_de_Ulloa_y_Ramirez_de_Haro
  AssignClass (947aa2da-5bb0-41c0-b142-1d21522c2056)
 Call ID: 947aa2da-5bb0-41c0-b142-1d21522c2056
  Args:
    type: :Person
    source: Gonzalo_Maria_de_Ulloa_y_Ramirez_de_Haro
  AddTriple (a8ec7ef9-16be-4176-bb40-6cd524d49f73)
 Call ID: a8ec7ef9-16be-4176-bb40-6cd524d49f73
  Args:
    source: Dona_Maria_del_Carmen_de_Ulloa_y_Suelves
    target: Gonzalo_Maria_de_Ulloa_y_Ramirez_de_Haro
    relation: :hasFather
  AssignClass (af6115aa-82bf-4fbd-ab24-a02ea4334e64)
 Call ID: af6115aa-82bf-4fbd-ab24-a02ea4334e64
  Args:
    type: :Woman
    source: Francoise_Cazaudehore
  AssignClass (7d1c190b-3e0d-4039-a6c2-e82b91936260)
 Call ID: 7d1c190b-3e0d-4039-a6c2-e82b91936260
  Args:
    type: :Person
    source: Francoise_Cazaudehore
  AssignClass (b33e727d-ca44-4a2f-b44e-39d320cffc4c)
 Call ID: b33e727d-ca44-4a2f-b44e-39d320cffc4c
  Args:
    source: Kristine_Dzidziguri
    type: :Woman
  AssignClass (ab211ded-152e-4bd7-a0e0-095e544edb97)
 Call ID: ab211ded-152e-4bd7-a0e0-095e544edb97
  Args:
    source: Kristine_Dzidziguri
    type: :Person
  AddTriple (c67aabf3-c0b4-4640-87a5-371c98d08bd3)
 Call ID: c67aabf3-c0b4-4640-87a5-371c98d08bd3
  Args:
    target: Kristine_Dzidziguri
    relation: :hasRelation
    source: Prince_Juan_Jorge_de_Bagration-Mukhrani
  AddLiteral (526e0012-9410-4f80-8401-cc3435af13fd)
 Call ID: 526e0012-9410-4f80-8401-cc3435af13fd
  Args:
    literal_value: 2014
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Prince_Juan_Jorge_de_Bagration-Mukhrani
  Finish (05e52c9d-1a23-4bb5-8b05-6b4d4333574e)
 Call ID: 05e52c9d-1a23-4bb5-8b05-6b4d4333574e
  Args: