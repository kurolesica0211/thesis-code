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
  AssignClass (d02be47e-5635-419a-9f6a-d123695f2ea6)
 Call ID: d02be47e-5635-419a-9f6a-d123695f2ea6
  Args:
    type: :Man
    source: :Prince_Juan_Jorge_de_Bagration-Mukhrani
  AssignClass (c916d3d1-e9b7-4d07-801b-bac26ff51b41)
 Call ID: c916d3d1-e9b7-4d07-801b-bac26ff51b41
  Args:
    type: :Person
    source: :Prince_Juan_Jorge_de_Bagration-Mukhrani
  AddLiteral (7ee1b565-1ce6-4ee6-992d-58003e5f7997)
 Call ID: 7ee1b565-1ce6-4ee6-992d-58003e5f7997
  Args:
    relation: :hasBirthYear
    literal_value: 1977
    source: :Prince_Juan_Jorge_de_Bagration-Mukhrani
    literal_type: xsd:integer
  AssignClass (a38db306-5e63-4572-9716-60a5fd54479e)
 Call ID: a38db306-5e63-4572-9716-60a5fd54479e
  Args:
    type: :Man
    source: :Prince_Bagrat_de_Bagration_y_de_Baviera
  AssignClass (60c89f52-d07b-4a11-a921-d77054104bc6)
 Call ID: 60c89f52-d07b-4a11-a921-d77054104bc6
  Args:
    type: :Person
    source: :Prince_Bagrat_de_Bagration_y_de_Baviera
  AddTriple (6b798971-18a8-4137-8654-4bbb7a30d11d)
 Call ID: 6b798971-18a8-4137-8654-4bbb7a30d11d
  Args:
    target: :Prince_Bagrat_de_Bagration_y_de_Baviera
    relation: :hasFather
    source: :Prince_Juan_Jorge_de_Bagration-Mukhrani
  AssignClass (10e6cfa2-834d-4e12-9ec2-de9cd948e773)
 Call ID: 10e6cfa2-834d-4e12-9ec2-de9cd948e773
  Args:
    type: :Woman
    source: :Dona_Maria_del_Carmen_de_Ulloa_y_Suelves
  AssignClass (50638885-8953-4289-a4e2-75ee8a496426)
 Call ID: 50638885-8953-4289-a4e2-75ee8a496426
  Args:
    type: :Person
    source: :Dona_Maria_del_Carmen_de_Ulloa_y_Suelves
  AddTriple (82c8ea73-2375-4a74-97c5-1a87c045befe)
 Call ID: 82c8ea73-2375-4a74-97c5-1a87c045befe
  Args:
    relation: :hasMother
    target: :Dona_Maria_del_Carmen_de_Ulloa_y_Suelves
    source: :Prince_Juan_Jorge_de_Bagration-Mukhrani
  AssignClass (fb2dcf5c-b460-4c63-8dc7-1e96e8b45b22)
 Call ID: fb2dcf5c-b460-4c63-8dc7-1e96e8b45b22
  Args:
    type: :Man
    source: :Prince_Irakli_Bagration_of_Mukhrani
  AssignClass (128f24c8-34f7-4f83-a4d5-17843ed1b54f)
 Call ID: 128f24c8-34f7-4f83-a4d5-17843ed1b54f
  Args:
    type: :Person
    source: :Prince_Irakli_Bagration_of_Mukhrani
  AddTriple (9c2301ad-7d64-46d2-905d-589ec3399ba4)
 Call ID: 9c2301ad-7d64-46d2-905d-589ec3399ba4
  Args:
    source: :Prince_Bagrat_de_Bagration_y_de_Baviera
    relation: :hasFather
    target: :Prince_Irakli_Bagration_of_Mukhrani
  AssignClass (64db70ef-a449-4e26-946d-d1ea426d6962)
 Call ID: 64db70ef-a449-4e26-946d-d1ea426d6962
  Args:
    type: :Woman
    source: :Infanta_Maria_de_las_Mercedes_of_Spain
  AssignClass (e83d26ae-3238-4ef2-bd28-7fb13461802c)
 Call ID: e83d26ae-3238-4ef2-bd28-7fb13461802c
  Args:
    type: :Person
    source: :Infanta_Maria_de_las_Mercedes_of_Spain
  AddTriple (6b933632-9313-4776-a3b5-d3b250a447eb)
 Call ID: 6b933632-9313-4776-a3b5-d3b250a447eb
  Args:
    target: :Infanta_Maria_de_las_Mercedes_of_Spain
    relation: :hasMother
    source: :Prince_Bagrat_de_Bagration_y_de_Baviera
  AssignClass (38d56c8a-4de7-42bf-9614-6a8eb0f9710f)
 Call ID: 38d56c8a-4de7-42bf-9614-6a8eb0f9710f
  Args:
    type: :Man
    source: :Gonzalo_Maria_de_Ulloa_y_Ramirez_de_Haro
  AssignClass (178b0182-358a-467a-8367-38f330fa2d0a)
 Call ID: 178b0182-358a-467a-8367-38f330fa2d0a
  Args:
    type: :Person
    source: :Gonzalo_Maria_de_Ulloa_y_Ramirez_de_Haro
  AddTriple (dabeee27-0513-4719-9a27-2553bb0adf44)
 Call ID: dabeee27-0513-4719-9a27-2553bb0adf44
  Args:
    source: :Dona_Maria_del_Carmen_de_Ulloa_y_Suelves
    target: :Gonzalo_Maria_de_Ulloa_y_Ramirez_de_Haro
    relation: :hasFather
  AssignClass (ecf739d2-6636-4d7b-b25c-b4fa25a7f8ff)
 Call ID: ecf739d2-6636-4d7b-b25c-b4fa25a7f8ff
  Args:
    type: :Woman
    source: :Francoise_Cazaudehore
  AssignClass (d535b496-de8e-458c-b39c-7682cbef25c6)
 Call ID: d535b496-de8e-458c-b39c-7682cbef25c6
  Args:
    type: :Person
    source: :Francoise_Cazaudehore
  AssignClass (6738d3fe-2267-4d91-bb80-04b0a7dd9751)
 Call ID: 6738d3fe-2267-4d91-bb80-04b0a7dd9751
  Args:
    type: :Woman
    source: :Kristine_Dzidziguri
  AssignClass (0ab1a402-dc10-4162-9ad2-4bcb713542d7)
 Call ID: 0ab1a402-dc10-4162-9ad2-4bcb713542d7
  Args:
    type: :Person
    source: :Kristine_Dzidziguri
  AddLiteral (3803501d-1fb6-458b-bd03-3774211903b1)
 Call ID: 3803501d-1fb6-458b-bd03-3774211903b1
  Args:
    relation: :hasMarriageYear
    literal_value: 2014
    source: :Prince_Juan_Jorge_de_Bagration-Mukhrani
    literal_type: xsd:integer
  AddTriple (3f1f41c4-4bed-449d-89e8-2b37798954d1)
 Call ID: 3f1f41c4-4bed-449d-89e8-2b37798954d1
  Args:
    target: :Kristine_Dzidziguri
    relation: :hasRelation
    source: :Prince_Juan_Jorge_de_Bagration-Mukhrani
  AssignClass (4a36a296-92ba-4755-a771-78ccbea5e779)
 Call ID: 4a36a296-92ba-4755-a771-78ccbea5e779
  Args:
    type: :Man
    source: :Prince_Ferdinand_of_Bavaria
  AssignClass (83df6652-58b4-47c6-b7f3-00fb96afc50a)
 Call ID: 83df6652-58b4-47c6-b7f3-00fb96afc50a
  Args:
    type: :Person
    source: :Prince_Ferdinand_of_Bavaria
  AddTriple (d417916f-f35e-4a58-a878-c7e75e4fcb09)
 Call ID: d417916f-f35e-4a58-a878-c7e75e4fcb09
  Args:
    source: :Infanta_Maria_de_las_Mercedes_of_Spain
    target: :Prince_Ferdinand_of_Bavaria
    relation: :hasFather
  AssignClass (43aa1a61-922a-4770-baab-df4412fe63e4)
 Call ID: 43aa1a61-922a-4770-baab-df4412fe63e4
  Args:
    type: :Man
    source: :Alfonso_XII_of_Spain
  AssignClass (f8d10522-a143-4888-9a5d-04e46ebb4c32)
 Call ID: f8d10522-a143-4888-9a5d-04e46ebb4c32
  Args:
    type: :Person
    source: :Alfonso_XII_of_Spain
  AssignClass (eb2288a2-c70f-4933-8b05-ae22c3d929ad)
 Call ID: eb2288a2-c70f-4933-8b05-ae22c3d929ad
  Args:
    type: :Man
    source: :Alfonso_XIII_of_Spain
  AssignClass (60941832-6fcc-41dc-839f-a4fbb82381a8)
 Call ID: 60941832-6fcc-41dc-839f-a4fbb82381a8
  Args:
    type: :Person
    source: :Alfonso_XIII_of_Spain
  Finish (8b1de604-6d3a-4b4c-ac5a-45946cca532b)
 Call ID: 8b1de604-6d3a-4b4c-ac5a-45946cca532b
  Args: