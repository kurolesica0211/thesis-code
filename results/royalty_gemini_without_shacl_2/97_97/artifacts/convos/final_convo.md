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
Descendants of Prince Felix and also members of the Grand Ducal Family of Luxembourg:


Princess Joan


Descendants of Prince René:


Princess Maria Pia


Princess Marina


Descendants of Prince Louis:


Prince RémyPrincess Elisabeth


Princess Chantal
Prince JeanPrincess Virginia


Princess Beatrix*


Princess Margriet*Pieter van Vollenhoven*


Princess Margarita of Bourbon-Parma, Countess of Colorno (Dutch: Margarita Maria Beatrix Prinses de Bourbon de Parme; born 13 October 1972), is the eldest daughter of Princess Irene of the Netherlands and Carlos Hugo, Duke of Parma.
She is a member of the House of Bourbon-Parma as well an extended member of the Dutch royal family.
Per a 1996 royal decree issued by Queen Beatrix, she is entitled to the style and title Her Royal Highness Princess Margarita de Bourbon de Parme in the Netherlands as a member of the extended royal family.
Early life

Born in Nijmegen, she is the twin sister of Prince Jaime.
She also has an elder brother, Prince Carlos, and a younger sister, Princess Carolina.
Her godparents are Queen Beatrix of the Netherlands (maternal aunt) and Prince Sixtus Henry of Bourbon-Parma (paternal uncle).
She is the eldest granddaughter of Queen Juliana and Prince Bernhard.
Together with her mother and her siblings she moved from Spain to The Netherlands, to live with her grandparents, Queen Juliana of the Netherlands and Prince Bernhard of Lippe-Biesterfeld at Baarn.
Margarita studied Cultural Anthropology at the Vrije Universiteit of Amsterdam and is an interior decorator.
First marriage and controversy

On 19 June 2001, Princess Margarita married the entrepreneur Edwin Karel Willem de Roy van Zuydewijn, member of a Dutch patrician family.
In 2003, a series of incidents became known as the Margarita-affair.
Margarita and her husband accused the Dutch Royal House and the Dutch secret service of obstructing the affairs of Fincentives, the company of de Roy van Zuydewijn.
The couple's home was the Bartas Castle in Saint-Georges, Gers, France, but by 2004 the princess was increasingly seen more often in Amsterdam than there.
Because of the quarrels between the princess and the Dutch Royal family during the Margarita-affair, she was not welcome at the marriage of her cousin Willem-Alexander, Prince of Orange to Máxima Zorreguieta, or at the funeral of her uncle, Prince Claus of the Netherlands.
On 20 February 2023, Princess Margarita and Ten Cate announced their divorce.
Together they have two daughters:


Margarita currently lives in Wassenaar.
Titles, styles and honours

Already a ducal princess from birth, her father bestowed on 2 September 1996 the substantive title Contessa di Colorno (Countess of Colorno) upon her.
The same year she was incorporated into the Dutch nobility by her aunt Queen Beatrix, with the highest noble title Prinses de Bourbon de Parme (Princess of Bourbon-Parma) and styled Hare Koninklijke Hoogheid (Her Royal Highness).
She does not belong to the House of Orange-Nassau or the limited Dutch royal house, but as a granddaughter of Queen Juliana, she is officially a member of the more extended Dutch royal family.
Ancestry

References

External links

2 also Princess of Lippe-Biesterfeld



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
  AssignClass (31c417f4-2059-445e-b03a-5a25290014cb)
 Call ID: 31c417f4-2059-445e-b03a-5a25290014cb
  Args:
    type: :Woman
    source: Princess_Margarita_of_Bourbon-Parma
  AssignClass (9f0ca5aa-97d8-4c7b-9c99-c0244b751cb8)
 Call ID: 9f0ca5aa-97d8-4c7b-9c99-c0244b751cb8
  Args:
    type: :Person
    source: Princess_Margarita_of_Bourbon-Parma
  AssignClass (21d3b852-5574-4c90-8d8d-abbceee95be2)
 Call ID: 21d3b852-5574-4c90-8d8d-abbceee95be2
  Args:
    type: :Woman
    source: Princess_Irene_of_the_Netherlands
  AssignClass (564e525f-cbcc-4ef1-bf6b-2599619a94f5)
 Call ID: 564e525f-cbcc-4ef1-bf6b-2599619a94f5
  Args:
    type: :Ancestor
    source: Princess_Irene_of_the_Netherlands
  AssignClass (0f77902d-fd88-4344-bb6e-dc6edde78e51)
 Call ID: 0f77902d-fd88-4344-bb6e-dc6edde78e51
  Args:
    type: :Man
    source: Carlos_Hugo_Duke_of_Parma
  AssignClass (eac315f3-3434-4d62-b6be-a7a38ee38080)
 Call ID: eac315f3-3434-4d62-b6be-a7a38ee38080
  Args:
    type: :Ancestor
    source: Carlos_Hugo_Duke_of_Parma
  AddTriple (71149910-32ea-46e6-9d25-e57566e6129f)
 Call ID: 71149910-32ea-46e6-9d25-e57566e6129f
  Args:
    relation: :isDaughterOf
    target: Princess_Irene_of_the_Netherlands
    source: Princess_Margarita_of_Bourbon-Parma
  AddTriple (04ff8683-f72a-4252-b931-eca09f2df5bf)
 Call ID: 04ff8683-f72a-4252-b931-eca09f2df5bf
  Args:
    source: Princess_Margarita_of_Bourbon-Parma
    target: Carlos_Hugo_Duke_of_Parma
    relation: :isDaughterOf
  AssignClass (26aa1eb9-2028-4243-9ab1-c28a99dc7cf3)
 Call ID: 26aa1eb9-2028-4243-9ab1-c28a99dc7cf3
  Args:
    type: :Man
    source: Prince_Jaime
  AssignClass (0bd0a7b5-07db-4af7-8301-435663fcdb55)
 Call ID: 0bd0a7b5-07db-4af7-8301-435663fcdb55
  Args:
    source: Prince_Jaime
    type: :Person
  AddTriple (8e88acdf-4ce2-49e5-9c57-f54830fe5e7f)
 Call ID: 8e88acdf-4ce2-49e5-9c57-f54830fe5e7f
  Args:
    source: Princess_Margarita_of_Bourbon-Parma
    target: Prince_Jaime
    relation: :isSiblingOf
  AssignClass (6c965f76-4ae8-4476-9185-03cb4687f721)
 Call ID: 6c965f76-4ae8-4476-9185-03cb4687f721
  Args:
    type: :Man
    source: Prince_Carlos
  AssignClass (a86d33b5-0786-48c7-b69a-812a50d27bfd)
 Call ID: a86d33b5-0786-48c7-b69a-812a50d27bfd
  Args:
    source: Prince_Carlos
    type: :Person
  AddTriple (18101864-4de9-42d0-9a48-9b37a79d1a5d)
 Call ID: 18101864-4de9-42d0-9a48-9b37a79d1a5d
  Args:
    source: Princess_Margarita_of_Bourbon-Parma
    relation: :isSiblingOf
    target: Prince_Carlos
  AssignClass (53becb8c-bcef-40b8-803a-e545cc4f6fa4)
 Call ID: 53becb8c-bcef-40b8-803a-e545cc4f6fa4
  Args:
    type: :Woman
    source: Princess_Carolina
  AssignClass (d9119c84-d065-4ad3-8af6-dbcaf1eeddbc)
 Call ID: d9119c84-d065-4ad3-8af6-dbcaf1eeddbc
  Args:
    source: Princess_Carolina
    type: :Person
  AddTriple (dfa410df-37de-45c1-956b-7bc09cfecbbc)
 Call ID: dfa410df-37de-45c1-956b-7bc09cfecbbc
  Args:
    source: Princess_Margarita_of_Bourbon-Parma
    relation: :isSiblingOf
    target: Princess_Carolina
  AssignClass (6b8f6bfb-67bd-4b40-a53f-05a225cb8786)
 Call ID: 6b8f6bfb-67bd-4b40-a53f-05a225cb8786
  Args:
    type: :Woman
    source: Queen_Juliana
  AssignClass (81e03ca4-58c7-4cec-a682-59bfa6966a85)
 Call ID: 81e03ca4-58c7-4cec-a682-59bfa6966a85
  Args:
    source: Queen_Juliana
    type: :Ancestor
  AssignClass (dbbca70e-b751-4868-a96d-a84ae0f42958)
 Call ID: dbbca70e-b751-4868-a96d-a84ae0f42958
  Args:
    source: Prince_Bernhard
    type: :Man
  AssignClass (352b2fd6-4dd6-4a38-88fb-cae1f763ce27)
 Call ID: 352b2fd6-4dd6-4a38-88fb-cae1f763ce27
  Args:
    source: Prince_Bernhard
    type: :Ancestor
  AddTriple (904b85f1-935a-436a-95d2-0194728decd9)
 Call ID: 904b85f1-935a-436a-95d2-0194728decd9
  Args:
    source: Princess_Irene_of_the_Netherlands
    target: Queen_Juliana
    relation: :isDaughterOf
  AddTriple (225dade7-9324-4590-b8f6-78076691a647)
 Call ID: 225dade7-9324-4590-b8f6-78076691a647
  Args:
    target: Prince_Bernhard
    relation: :isDaughterOf
    source: Princess_Irene_of_the_Netherlands
  AssignClass (8c0f6ff9-7b54-435b-aea3-dda4c36e7283)
 Call ID: 8c0f6ff9-7b54-435b-aea3-dda4c36e7283
  Args:
    type: :Woman
    source: Queen_Beatrix
  AssignClass (b7b0f15f-62c9-405a-8c65-f90377a06b25)
 Call ID: b7b0f15f-62c9-405a-8c65-f90377a06b25
  Args:
    source: Queen_Beatrix
    type: :Person
  AddTriple (edccb8ad-422a-4b75-9568-ddecdd64a8a2)
 Call ID: edccb8ad-422a-4b75-9568-ddecdd64a8a2
  Args:
    source: Queen_Beatrix
    target: Princess_Irene_of_the_Netherlands
    relation: :isSisterOf
  AssignClass (87798cae-6599-4457-b05b-bd4dc15df54f)
 Call ID: 87798cae-6599-4457-b05b-bd4dc15df54f
  Args:
    type: :Man
    source: Prince_Sixtus_Henry_of_Bourbon-Parma
  AssignClass (5c1a7aeb-f5f0-4c38-961b-61c04e9eb083)
 Call ID: 5c1a7aeb-f5f0-4c38-961b-61c04e9eb083
  Args:
    type: :Person
    source: Prince_Sixtus_Henry_of_Bourbon-Parma
  AddTriple (e4da399e-5086-4b94-8090-d55244250ffa)
 Call ID: e4da399e-5086-4b94-8090-d55244250ffa
  Args:
    target: Carlos_Hugo_Duke_of_Parma
    relation: :isBrotherOf
    source: Prince_Sixtus_Henry_of_Bourbon-Parma
  AssignClass (f2ca8659-8880-4745-9bb8-ba92715ad51a)
 Call ID: f2ca8659-8880-4745-9bb8-ba92715ad51a
  Args:
    source: Edwin_Karel_Willem_de_Roy_van_Zuydewijn
    type: :Man
  AssignClass (a16d4b04-7654-419f-9592-9b5c93794efd)
 Call ID: a16d4b04-7654-419f-9592-9b5c93794efd
  Args:
    type: :Person
    source: Edwin_Karel_Willem_de_Roy_van_Zuydewijn
  AddLiteral (adcaab2d-e498-4f13-b39f-5c880101d089)
 Call ID: adcaab2d-e498-4f13-b39f-5c880101d089
  Args:
    relation: :hasMarriageYear
    literal_value: 2001
    source: Princess_Margarita_of_Bourbon-Parma
    literal_type: xsd:integer
  AddLiteral (204d36f6-b029-47c4-8663-4987fa97bb33)
 Call ID: 204d36f6-b029-47c4-8663-4987fa97bb33
  Args:
    literal_value: 1972
    relation: :hasBirthYear
    source: Princess_Margarita_of_Bourbon-Parma
    literal_type: xsd:integer
  Finish (1e8a5a41-5710-4ad4-a027-4d2bfa35e8c8)
 Call ID: 1e8a5a41-5710-4ad4-a027-4d2bfa35e8c8
  Args: