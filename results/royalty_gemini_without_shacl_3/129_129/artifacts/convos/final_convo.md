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


Princess Carolina of Bourbon-Parma, Marchioness of Sala (born 23 June 1974), is the fourth and youngest child of Princess Irene of the Netherlands and Carlos Hugo, Duke of Parma.
She is a member of the House of Bourbon-Parma as well an extended member of the Dutch royal family.
Per a 1996 royal decree issued by Queen Beatrix, she is entitled to the style and title Her Royal Highness Princess Maria Carolina de Bourbon de Parme in The Netherlands as a member of the extended royal family.
Early life

Princess Carolina was born at 23 June 1974 in Nijmegen.
She has two older brothers, Prince Carlos, the head of the House of Bourbon-Parma, and Prince Jaime.
She also has one older sister, Princess Margarita.
She was baptised at the Castle of Lignières in France with Prince Claus of the Netherlands, Princess Christina of the Netherlands and Princess Marie des Neiges of Bourbon-Parma as her godparents.
She moved together with her mother and her brothers and sister to Soest, Netherlands, nearby the then residence of her grandparents the former Queen of the Netherlands Queen Juliana of the Netherlands and Prince Bernhard of Lippe-Biesterfeld.
Education and career

Princess Carolina studied political science at University of Amsterdam and Harvard University, and also has an M.Sc.
Marriage

On 9 January 2012, it was announced that Princess Carolina would marry Albert Alphons Ludgerus Brenninkmeijer (born 16 May 1974), a member of the wealthy Brenninkmeijer family.
The princess has been seen regularly at important events of the royal house of the Netherlands.
In 2001 she was one of the maids of honor at the wedding of Prince Constantijn and Petra Laurentien Brinkhorst; and during the baptism of their daughter, Countess Eloise of Orange-Nassau, she was the godmother of the child.
She was a witness at the church wedding of her cousin Prince Floris of Orange-Nassau, van Vollenhoven, and in 2010, was named as the godmother of Floris' second child, Eliane.


Titles, styles and honours

Already a ducal princess from birth, her father bestowed the substantive title Marchesa di Sala (Marchioness of Sala) upon her on 2 September 1996.
In 1996 she was incorporated into the Dutch nobility by her aunt Queen Beatrix, with the highest title of nobility Prinses de Bourbon de Parme (Princess of Bourbon-Parma) and styled Hare Koninklijke Hoogheid (Her Royal Highness).
She does not belong to the House of Orange-Nassau or the limited Dutch royal house, but as a granddaughter of Queen Juliana and first cousin of the present King Willem-Alexander, she is officially a member of the more extended Dutch royal family.
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
  AssignClass (1d67bd16-6fcf-4918-b9c8-33e6ea8d9b0a)
 Call ID: 1d67bd16-6fcf-4918-b9c8-33e6ea8d9b0a
  Args:
    type: :Woman
    source: :Princess_Carolina
  AssignClass (77277419-e252-4eef-8bbe-d50d2ce89922)
 Call ID: 77277419-e252-4eef-8bbe-d50d2ce89922
  Args:
    type: :Woman
    source: :Princess_Irene
  AssignClass (faf50afe-6515-49e4-b48e-a9c94b2344fa)
 Call ID: faf50afe-6515-49e4-b48e-a9c94b2344fa
  Args:
    type: :Man
    source: :Carlos_Hugo
  AddTriple (095b314f-2bd2-4144-95c5-a9910cd425f4)
 Call ID: 095b314f-2bd2-4144-95c5-a9910cd425f4
  Args:
    source: :Princess_Carolina
    relation: :isDaughterOf
    target: :Princess_Irene
  AddTriple (6eb5a00c-1107-415c-9efd-bea0b271246c)
 Call ID: 6eb5a00c-1107-415c-9efd-bea0b271246c
  Args:
    source: :Princess_Carolina
    relation: :isDaughterOf
    target: :Carlos_Hugo
  AddLiteral (4a658483-035b-46af-89e9-095c6c04f4d6)
 Call ID: 4a658483-035b-46af-89e9-095c6c04f4d6
  Args:
    literal_type: xsd:integer
    source: :Princess_Carolina
    literal_value: 1974
    relation: :hasBirthYear
  AssignClass (3d0337f1-4b01-4196-8f99-e1f805ae955b)
 Call ID: 3d0337f1-4b01-4196-8f99-e1f805ae955b
  Args:
    source: :Prince_Carlos
    type: :Man
  AssignClass (a5d386c8-2945-4e90-90e2-a6d6648a06da)
 Call ID: a5d386c8-2945-4e90-90e2-a6d6648a06da
  Args:
    type: :Man
    source: :Prince_Jaime
  AssignClass (fded6931-f2e6-4e8d-a396-ee08faabeefe)
 Call ID: fded6931-f2e6-4e8d-a396-ee08faabeefe
  Args:
    type: :Woman
    source: :Princess_Margarita
  AddTriple (2eeb87b8-fa11-43ac-b8f4-08e2aed6d467)
 Call ID: 2eeb87b8-fa11-43ac-b8f4-08e2aed6d467
  Args:
    target: :Prince_Carlos
    relation: :isSiblingOf
    source: :Princess_Carolina
  AddTriple (41fcd292-6c95-4c42-a74c-babec6273ba8)
 Call ID: 41fcd292-6c95-4c42-a74c-babec6273ba8
  Args:
    target: :Prince_Jaime
    source: :Princess_Carolina
    relation: :isSiblingOf
  AddTriple (f27237d3-459a-460e-9708-0eb4d8caf3b8)
 Call ID: f27237d3-459a-460e-9708-0eb4d8caf3b8
  Args:
    target: :Princess_Margarita
    source: :Princess_Carolina
    relation: :isSiblingOf
  AssignClass (bb950cec-1899-488b-8508-d798e8b85f72)
 Call ID: bb950cec-1899-488b-8508-d798e8b85f72
  Args:
    type: :Man
    source: :Albert_Brenninkmeijer
  AddLiteral (3ab5fdc6-0fda-4e3d-8e94-4c87ee2496d2)
 Call ID: 3ab5fdc6-0fda-4e3d-8e94-4c87ee2496d2
  Args:
    relation: :hasBirthYear
    literal_value: 1974
    source: :Albert_Brenninkmeijer
    literal_type: xsd:integer
  AssignClass (5a12415c-c3b6-4fb9-a0c5-2e720f59a140)
 Call ID: 5a12415c-c3b6-4fb9-a0c5-2e720f59a140
  Args:
    source: :Queen_Juliana
    type: :Woman
  AssignClass (c1493644-9eea-4487-b551-3ff1881fafff)
 Call ID: c1493644-9eea-4487-b551-3ff1881fafff
  Args:
    source: :Prince_Bernhard
    type: :Man
  AddTriple (996dd9af-93cd-4d6c-849f-faf0d72e28c7)
 Call ID: 996dd9af-93cd-4d6c-849f-faf0d72e28c7
  Args:
    relation: :isMotherOf
    source: :Queen_Juliana
    target: :Princess_Irene
  AddTriple (b7bce6c5-071d-45cd-a296-140fbaf5d67e)
 Call ID: b7bce6c5-071d-45cd-a296-140fbaf5d67e
  Args:
    target: :Princess_Irene
    relation: :isFatherOf
    source: :Prince_Bernhard
  AssignClass (1742ff48-606e-4880-ab02-a6da46820d4a)
 Call ID: 1742ff48-606e-4880-ab02-a6da46820d4a
  Args:
    type: :Man
    source: :Prince_Felix
  AssignClass (4aa86a6d-12ba-4db4-9cb0-81e37e0a506a)
 Call ID: 4aa86a6d-12ba-4db4-9cb0-81e37e0a506a
  Args:
    type: :Woman
    source: :Princess_Joan
  AddTriple (b64891db-dbdf-4702-adec-bc8d8b32c3ac)
 Call ID: b64891db-dbdf-4702-adec-bc8d8b32c3ac
  Args:
    source: :Princess_Joan
    relation: :isChildOf
    target: :Prince_Felix
  AssignClass (3920e9d2-b870-423e-8a77-b44d8f6a01ed)
 Call ID: 3920e9d2-b870-423e-8a77-b44d8f6a01ed
  Args:
    source: :Prince_Rene
    type: :Man
  AssignClass (342ea1bd-6f34-4c24-a8e6-93b76b2d10a2)
 Call ID: 342ea1bd-6f34-4c24-a8e6-93b76b2d10a2
  Args:
    type: :Woman
    source: :Princess_Maria_Pia
  AssignClass (7e629a04-2742-494e-99f4-c3506fbfbbde)
 Call ID: 7e629a04-2742-494e-99f4-c3506fbfbbde
  Args:
    source: :Princess_Marina
    type: :Woman
  AddTriple (04c9a83b-3a66-4b29-a01f-0c45d4572b8a)
 Call ID: 04c9a83b-3a66-4b29-a01f-0c45d4572b8a
  Args:
    target: :Prince_Rene
    relation: :isChildOf
    source: :Princess_Maria_Pia
  AddTriple (68511d1e-746b-4e99-9342-9ef9b1da68d4)
 Call ID: 68511d1e-746b-4e99-9342-9ef9b1da68d4
  Args:
    source: :Princess_Marina
    relation: :isChildOf
    target: :Prince_Rene
  AssignClass (395a2a0e-4ed8-4888-add9-579d7c46d4bc)
 Call ID: 395a2a0e-4ed8-4888-add9-579d7c46d4bc
  Args:
    source: :Prince_Louis
    type: :Man
  AssignClass (16c4713b-2396-4b6c-b5be-63e2586f926f)
 Call ID: 16c4713b-2396-4b6c-b5be-63e2586f926f
  Args:
    type: :Man
    source: :Prince_Remy
  AssignClass (3b0a9ebe-804f-42fc-b937-a0d7a6079960)
 Call ID: 3b0a9ebe-804f-42fc-b937-a0d7a6079960
  Args:
    type: :Woman
    source: :Princess_Elisabeth
  AssignClass (32949476-87d3-4f8f-96fa-e12ca9993fa5)
 Call ID: 32949476-87d3-4f8f-96fa-e12ca9993fa5
  Args:
    type: :Woman
    source: :Princess_Chantal
  AssignClass (495f5dfd-4b27-46a6-ab8a-dc70d30e5ad9)
 Call ID: 495f5dfd-4b27-46a6-ab8a-dc70d30e5ad9
  Args:
    type: :Man
    source: :Prince_Jean
  AssignClass (a2a3d7ca-68da-42bd-846a-d711f72e8457)
 Call ID: a2a3d7ca-68da-42bd-846a-d711f72e8457
  Args:
    source: :Princess_Virginia
    type: :Woman
  AssignClass (412ded9f-32ff-4051-8655-decb085ec5eb)
 Call ID: 412ded9f-32ff-4051-8655-decb085ec5eb
  Args:
    source: :Princess_Beatrix
    type: :Woman
  AssignClass (bc5d08e2-50f6-4766-a33a-cd415d79c690)
 Call ID: bc5d08e2-50f6-4766-a33a-cd415d79c690
  Args:
    source: :Princess_Margriet
    type: :Woman
  AssignClass (1e27a953-42ac-42c7-9242-f6f0595ad73e)
 Call ID: 1e27a953-42ac-42c7-9242-f6f0595ad73e
  Args:
    type: :Man
    source: :Pieter_van_Vollenhoven
  AddTriple (d0bb569c-926c-4661-9ca7-c9e3c25d441e)
 Call ID: d0bb569c-926c-4661-9ca7-c9e3c25d441e
  Args:
    source: :Prince_Remy
    relation: :isChildOf
    target: :Prince_Louis
  AddTriple (524838d7-1699-4256-98d1-494f184686f2)
 Call ID: 524838d7-1699-4256-98d1-494f184686f2
  Args:
    relation: :isChildOf
    source: :Princess_Elisabeth
    target: :Prince_Louis
  AddTriple (10b724ae-fc9e-47bc-8022-1aa13e4d099d)
 Call ID: 10b724ae-fc9e-47bc-8022-1aa13e4d099d
  Args:
    relation: :isChildOf
    source: :Princess_Chantal
    target: :Prince_Louis
  AddTriple (15919ea1-e337-477e-90fc-f67082a212c7)
 Call ID: 15919ea1-e337-477e-90fc-f67082a212c7
  Args:
    relation: :isChildOf
    source: :Prince_Jean
    target: :Prince_Louis
  AddTriple (5b2c4c08-f454-4f19-8360-353510708253)
 Call ID: 5b2c4c08-f454-4f19-8360-353510708253
  Args:
    source: :Princess_Virginia
    relation: :isChildOf
    target: :Prince_Louis
  AddTriple (6d464fe7-a035-466b-9a52-e7371804f515)
 Call ID: 6d464fe7-a035-466b-9a52-e7371804f515
  Args:
    target: :Prince_Louis
    source: :Princess_Beatrix
    relation: :isChildOf
  AddTriple (dc117c97-8703-48dd-8370-da62a7506d4b)
 Call ID: dc117c97-8703-48dd-8370-da62a7506d4b
  Args:
    target: :Prince_Louis
    source: :Princess_Margriet
    relation: :isChildOf
  Finish (5f8bbca6-d1b0-4d58-a156-01a575334096)
 Call ID: 5f8bbca6-d1b0-4d58-a156-01a575334096
  Args: